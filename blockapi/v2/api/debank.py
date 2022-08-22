import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from eth_utils import to_checksum_address

from blockapi.utils.num import decimals_to_raw
from blockapi.v2.base import ApiOptions, BlockchainApi, IBalance, IPortfolio
from blockapi.v2.models import (
    DEBANK_ASSET_TYPES,
    DEBANK_BLOCKCHAIN,
    AssetType,
    BalanceItem,
    Blockchain,
    Coin,
    CoinInfo,
    Pool,
    Protocol,
)

logger = logging.getLogger(__name__)


REWARD_ASSET_TYPE_CONVERT = {
    AssetType.LENDING: AssetType.LENDING_REWARD,
    AssetType.STAKED: AssetType.REWARDS,
    AssetType.FARMING: AssetType.REWARDS,
    AssetType.YIELD: AssetType.REWARDS,
}


class DebankProtocolParser:
    def parse(self, response: List) -> Dict[str, Protocol]:
        protocols = {}
        for item in response:
            protocol = self.parse_item(item)
            protocols[protocol.protocol_id] = protocol

        return protocols

    @staticmethod
    def parse_item(item) -> Protocol:
        return Protocol.from_api(
            protocol_id=item.get('id'),
            chain=item.get('chain'),
            name=item.get('name'),
            user_deposit=item.get('tvl'),
            site_url=item.get('site_url'),
            logo_url=item.get('logo_url'),
            has_supported_portfolio=item.get('has_supported_portfolio', False),
        )


class DebankProtocolCache:
    def __init__(self, timeout: int = 3600):
        self._timeout: int = timeout
        self._data: Dict[str, Protocol] = {}
        self._timelimit = datetime.now()

    def invalidate(self):
        self._timelimit = datetime.now()

    def needs_update(self) -> bool:
        return datetime.now() >= self._timelimit

    def update(self, data: Dict[str, Protocol]) -> None:
        self._timelimit = datetime.now() + timedelta(seconds=self._timeout)
        self._data = data

    def get(self, key: str) -> Optional[Protocol]:
        protocol = self._data.get(key)
        if protocol is None:
            logger.debug("Protocol '%s' not found.", key)

        return protocol


class DebankBalanceParser:
    def __init__(self, protocol_cache: DebankProtocolCache):
        self._protocols = protocol_cache

    def parse(
        self,
        response: List,
        asset_type: AssetType = AssetType.AVAILABLE,
        is_wallet: bool = True,
        token_set: Optional[List[str]] = None,
    ) -> List[BalanceItem]:
        items = []
        for item in response:
            balance = self.parse_item(item, asset_type, is_wallet, token_set)
            if balance is not None:
                items.append(balance)

        return items

    def parse_item(
        self,
        raw_balance: dict,
        asset_type: AssetType = AssetType.AVAILABLE,
        is_wallet: bool = True,
        token_set: Optional[List[str]] = None,
    ) -> Optional[BalanceItem]:
        raw_amount = raw_balance.get('raw_amount', 0)
        amount = raw_balance.get('amount', 0)

        if raw_amount == 0 and amount == 0:
            logger.debug(
                "Skipping coin: '%s' - balance is zero.",
                raw_balance.get("name"),
            )

            return None

        symbol = self._get_symbol(raw_balance)

        coin = Coin.from_api(
            symbol=symbol,
            name=raw_balance.get('name'),
            decimals=raw_balance.get('decimals', 0),
            blockchain=self._convert_blockchain(raw_balance.get('chain')),
            address=make_checksum_address(raw_balance.get('id')),
            standards=[],
            protocol_id=raw_balance.get('protocol_id'),
            info=CoinInfo(logo_url=raw_balance.get('logo_url')),
        )

        if asset_type == AssetType.INVESTMENT and amount < 0:
            asset_type = AssetType.DEBT
            amount = -amount

        if raw_amount == 0 and amount != 0:
            raw_amount = decimals_to_raw(amount, coin.decimals)

        balance = BalanceItem.from_api(
            balance_raw=raw_amount,
            coin=coin,
            asset_type=asset_type,
            last_updated=raw_balance.get('time_at'),
            raw=raw_balance,
            protocol=self._protocols.get(raw_balance.get('protocol_id', '')),
            is_wallet=is_wallet,
            token_set=token_set,
        )

        return balance

    @staticmethod
    def _get_symbol(raw_balance: dict) -> str:
        return (
            raw_balance.get('display_symbol')
            or raw_balance.get('optimized_symbol')
            or raw_balance.get('symbol')
        )

    @staticmethod
    def _convert_blockchain(chain):
        result = DEBANK_BLOCKCHAIN.get(chain)
        if result is not None:
            return result

        try:
            return Blockchain(chain)
        except ValueError:
            logger.warning(f"Unknown blockchain '{chain}'")
            return chain


def make_checksum_address(address: str) -> str:
    try:
        return to_checksum_address(address)
    except ValueError as e:
        logger.warning(f'Cannot parse address "{address}", error: {e}')
        return None


class DebankPortfolioParser:
    def __init__(
        self, protocol_parser: DebankProtocolParser, balance_parser: DebankBalanceParser
    ):
        self._protocol_parser = protocol_parser
        self._balance_parser = balance_parser

    def parse(self, response: List) -> List[Pool]:
        items = []
        for item in response:
            parsed = self.parse_items(item)
            items.extend(parsed)

        return items

    def parse_items(self, raw_portfolio) -> List[Pool]:
        root_protocol = self._protocol_parser.parse_item(raw_portfolio)
        pools = self._parse_portfolio_item_list(
            raw_portfolio.get('portfolio_item_list', []), root_protocol
        )

        return pools

    def _parse_portfolio_item_list(
        self, raw_portfolio_items: List[Dict], root_protocol
    ) -> List[Pool]:
        items = []
        pools = {}
        for item in raw_portfolio_items:
            pool = self._parse_portfolio_item(item, root_protocol, pools)
            if pool.pool_id:
                pools[pool.pool_id] = pool

            items.append(pool)

        return items

    def _parse_portfolio_item(
        self, item: Dict, pool_protocol: Protocol, pools: Dict[str, Pool]
    ) -> Pool:
        pool_id = self._get_pool_id(item)
        detail = item.get('detail', {})

        health_rate = detail.get('health_rate')
        locked_until = detail.get('unlock_at')

        asset_type = self._parse_asset_type(item.get('name'))
        borrow_type = self._get_borrow_asset_type(asset_type)
        reward_type = self._get_reward_asset_type(asset_type)

        items = []

        tokens = self._update_items(items, detail, 'supply_token_list', asset_type)
        self._update_items(items, detail, 'borrow_token_list', borrow_type, tokens)
        self._update_items(items, detail, 'reward_token_list', reward_type, tokens)
        self._update_items(items, detail, 'token_list', asset_type)

        pool = pools.get(pool_id)

        if pool is None:
            pool = Pool.from_api(
                pool_id=pool_id,
                protocol=pool_protocol,
                locked_until=locked_until,
                health_rate=health_rate,
                items=items,
                token_set=detail.get('description'),
                project_id=self._get_from_pool(item, 'project_id'),
                adapter_id=self._get_from_pool(item, 'adapter_id'),
            )
        else:
            pool.append_items(items)

        return pool

    def _update_items(
        self,
        items: List[BalanceItem],
        detail: dict,
        key: str,
        asset_type: AssetType,
        tokens: Optional[List[str]] = None,
    ):
        raw_balances = detail.get(key, [])
        if tokens is None:
            tokens = sorted(
                list(set([self._balance_parser._get_symbol(b) for b in raw_balances]))
            )

        balances = self._balance_parser.parse(
            raw_balances,
            asset_type,
            False,
            token_set=tokens if len(raw_balances) > 1 else None,
        )
        items.extend(balances)

        return tokens

    @staticmethod
    def _get_from_pool(item: dict, key: str) -> Optional[str]:
        pool = item.get('pool')
        if pool is None:
            return None

        return pool.get(key)

    @staticmethod
    def _get_pool_id(item: dict) -> str:
        pool = item.get('pool')
        pool_id = pool.get('id') if pool else item.get('pool_id')
        return pool_id

    @staticmethod
    def _parse_asset_type(type_: str) -> Optional[AssetType]:
        # list of valid types: https://docs.open.debank.com/en/reference/api-models/portfolioitemobject
        if type_ is None:
            return AssetType.AVAILABLE

        try:
            lower = type_.lower()
            asset_type = DEBANK_ASSET_TYPES.get(lower)
            if asset_type:
                return asset_type

            return AssetType(lower)
        except ValueError as ve:
            logger.error(ve)
            return AssetType.AVAILABLE

    @staticmethod
    def _get_borrow_asset_type(asset_type):
        if asset_type == AssetType.LENDING:
            return AssetType.LENDING_BORROW

        return asset_type

    @staticmethod
    def _get_reward_asset_type(asset_type):
        return REWARD_ASSET_TYPE_CONVERT.get(asset_type, asset_type)


class DebankApi(BlockchainApi, IBalance, IPortfolio):
    """
    DeBank OpenApi: https://openapi.debank.com/docs
    """

    API_BASE_URL = 'https://openapi.debank.com'
    API_BASE_RATE_LIMIT = 0.05  # 20 req / s

    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url=API_BASE_URL,
        rate_limit=API_BASE_RATE_LIMIT,
    )

    supported_requests = {
        'get_balance': '/v1/user/token_list?id={address}&is_all={is_all}',
        'get_portfolio': '/v1/user/complex_protocol_list?id={address}',
        'get_protocols': '/v1/protocol/list',
    }

    default_protocol_cache = DebankProtocolCache()

    def __init__(
        self, is_all: bool, protocol_cache: Optional[DebankProtocolCache] = None
    ):
        super().__init__()

        self._is_all = bool(is_all)
        self._protocol_cache = protocol_cache or self.default_protocol_cache
        self._balance_parser = DebankBalanceParser(self._protocol_cache)
        self._protocol_parser = DebankProtocolParser()
        self._portfolio_parser = DebankPortfolioParser(
            self._protocol_parser, self._balance_parser
        )

    def get_balance(self, address: str) -> List[BalanceItem]:
        self._maybe_update_protocols()
        response = self.get('get_balance', address=address, is_all=self._is_all)
        if self._has_error(response):
            return []

        return self._balance_parser.parse(response)

    def get_protocols(self) -> Dict[str, Protocol]:
        response = self.get('get_protocols')
        if self._has_error(response):
            return {}

        return self._protocol_parser.parse(response)

    def get_portfolio(self, address: str) -> List[Pool]:
        self._maybe_update_protocols()
        response = self.get('get_portfolio', address=address)
        if self._has_error(response):
            return []

        return self._portfolio_parser.parse(response)

    def _maybe_update_protocols(self):
        if self._protocol_cache.needs_update():
            self._protocol_cache.update(self.get_protocols())

    @staticmethod
    def _has_error(response: Union[List, Dict]) -> bool:
        if isinstance(response, list):
            return False

        error = response.get('errors')
        message = response.get('message')
        if message is not None:
            logger.error('DebankApi Error: %s', message)

        if error is not None:
            err_id = error.get('id')
            if err_id is not None:
                logger.error(err_id)

        return message is not None or error is not None

    def __repr__(self):
        return f"{self.__class__.__name__}"
