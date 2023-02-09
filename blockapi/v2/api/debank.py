import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from eth_utils import to_checksum_address
from pydantic import BaseModel, validator

from blockapi.utils.num import decimals_to_raw
from blockapi.v2.api.debank_maps import (
    ALL_COINS,
    DEBANK_ASSET_TYPES,
    NATIVE_COIN_MAP,
    REWARD_ASSET_TYPE_MAP,
)
from blockapi.v2.base import ApiOptions, CustomizableBlockchainApi, IBalance, IPortfolio
from blockapi.v2.blockchain_mapping import get_blockchain_from_debank_chain
from blockapi.v2.models import (
    AssetType,
    BalanceItem,
    Blockchain,
    Coin,
    CoinInfo,
    Pool,
    Protocol,
    TokenRole,
)

logger = logging.getLogger(__name__)


class DebankModelBalanceItem(BaseModel):
    id: str
    chain: str
    name: str
    symbol: str
    display_symbol: Optional[str]
    optimized_symbol: Optional[str]
    decimals: int
    logo_url: Optional[str]
    protocol_id: Optional[str]
    time_at: Optional[float]
    amount: float
    raw_amount: Optional[float]
    raw_value: Optional[dict]


class DebankModelPoolItemDetail(BaseModel):
    description: Optional[str]
    health_rate: Optional[float]
    unlock_at: Optional[float]
    token_list: Optional[List[Dict]]
    supply_token_list: Optional[List[Dict]]
    borrow_token_list: Optional[List[Dict]]
    reward_token_list: Optional[List[Dict]]


class DebankModelPoolItem(BaseModel):
    id: str
    project_id: str
    adapter_id: str


class DebankModelPortfolioItem(BaseModel):
    name: str
    detail: DebankModelPoolItemDetail
    pool_id: Optional[str]
    pool: Optional[DebankModelPoolItem]

    @validator('pool')
    def require_pool_or_pool_id(cls, v, values, **kwargs):
        if v is not None:
            return v

        if not 'pool_id' in values or values['pool_id'] is None:
            raise ValueError('either pool or pool_id must have a value')

        return v


class DebankModelProtocol(BaseModel):
    id: str
    chain: str
    name: str
    site_url: Optional[str]
    logo_url: Optional[str]
    has_supported_portfolio: Optional[bool] = False
    tvl: Optional[float]


class DebankModelPortfolio(DebankModelProtocol):
    portfolio_item_list: List[DebankModelPortfolioItem]


class DebankProtocolParser:
    def parse(self, response: List) -> Dict[str, Protocol]:
        protocols = {}
        for item in response:
            model = DebankModelProtocol(**item)
            protocol = self.parse_item(model)
            if protocol:
                protocols[protocol.protocol_id] = protocol

        return protocols

    @staticmethod
    def parse_item(item: DebankModelProtocol) -> Optional[Protocol]:
        blockchain = get_blockchain_from_debank_chain(item.chain)
        if not blockchain:
            logger.warning(f'No blockchain found for protocol {item.id}')
            return None

        return Protocol.from_api(
            protocol_id=item.id,
            chain=blockchain,
            name=item.name,
            user_deposit=item.tvl,
            site_url=item.site_url,
            logo_url=item.logo_url,
            has_supported_portfolio=item.has_supported_portfolio,
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
        token_role: Optional[TokenRole] = None,
        pool_id: Optional[str] = None,
    ) -> List[BalanceItem]:
        items = []
        for item in response:
            balance_item = DebankModelBalanceItem(**item)
            balance_item.raw_value = item

            balance = self.parse_item(
                balance_item, asset_type, is_wallet, token_set, token_role, pool_id
            )
            if balance is not None:
                items.append(balance)

        return items

    def parse_item(
        self,
        balance_item: DebankModelBalanceItem,
        asset_type: AssetType = AssetType.AVAILABLE,
        is_wallet: bool = True,
        token_set: Optional[List[str]] = None,
        token_role: Optional[TokenRole] = None,
        pool_id: Optional[str] = None,
    ) -> Optional[BalanceItem]:
        raw_amount = balance_item.raw_amount or 0
        amount = balance_item.amount or 0

        if raw_amount == 0 and amount == 0:
            logger.debug(
                "Skipping balance item: '%s' - balance is zero.",
                balance_item.name,
            )

            return None

        symbol = self.get_symbol(balance_item)
        coin = self.get_coin(balance_item, symbol)

        if not coin:
            logger.error(
                f'DeBank: Skipping balance - could not parse coin "{balance_item.id} {balance_item.chain} {balance_item.symbol}". Amount={amount}'
            )
            return None

        if not coin.blockchain:
            logger.error(
                f'DeBank: Skipping balance - could not parse blockchain "{balance_item.chain}". Amount={amount} (raw={raw_amount})'
            )
            return None

        if asset_type == AssetType.INVESTMENT and amount < 0:
            asset_type = AssetType.DEBT
            amount = -amount

        if raw_amount == 0 and amount != 0:
            raw_amount = decimals_to_raw(amount, coin.decimals)

        balance = BalanceItem.from_api(
            balance_raw=raw_amount,
            coin=coin,
            asset_type=asset_type,
            last_updated=balance_item.time_at,
            raw=balance_item.raw_value,
            protocol=self._protocols.get(balance_item.protocol_id),
            is_wallet=is_wallet,
            token_set=token_set,
            token_role=token_role,
            pool_id=pool_id,
        )

        return balance

    def get_coin(self, balance_item: DebankModelBalanceItem, symbol: str) -> Coin:
        address = balance_item.id
        blockchain = get_blockchain_from_debank_chain(balance_item.chain)
        coin = NATIVE_COIN_MAP.get(address)

        if coin is not None and coin.blockchain == blockchain and coin.symbol == symbol:
            return coin

        valid_address = make_checksum_address(address)

        if valid_address:
            return Coin.from_api(
                symbol=symbol,
                name=balance_item.name,
                decimals=balance_item.decimals,
                blockchain=blockchain,
                address=valid_address,
                standards=[],
                protocol_id=balance_item.protocol_id,
                info=CoinInfo(logo_url=balance_item.logo_url),
            )

        return ALL_COINS.get(symbol.lower())

    @staticmethod
    def get_symbol(raw_balance: DebankModelBalanceItem) -> str:
        return (
            raw_balance.display_symbol
            or raw_balance.optimized_symbol
            or raw_balance.symbol
        )


def make_checksum_address(address: str) -> Optional[str]:
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
            portfolio = DebankModelPortfolio(**item)
            parsed = self.parse_items(portfolio)
            items.extend(parsed)

        return items

    def parse_items(self, raw_portfolio: DebankModelPortfolio) -> List[Pool]:
        root_protocol = self._protocol_parser.parse_item(raw_portfolio)
        pools = self._parse_portfolio_item_list(
            raw_portfolio.portfolio_item_list or [], root_protocol
        )

        return pools

    def _parse_portfolio_item_list(
        self,
        raw_portfolio_items: List[DebankModelPortfolioItem],
        root_protocol: Protocol,
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
        self,
        item: DebankModelPortfolioItem,
        pool_protocol: Protocol,
        pools: Dict[str, Pool],
    ) -> Pool:
        pool_id = self._get_pool_id(item)
        detail = item.detail

        health_rate = detail.health_rate
        locked_until = detail.unlock_at

        asset_type = self._parse_asset_type(item.name)
        borrow_type = self._get_borrow_asset_type(asset_type)
        reward_type = self._get_reward_asset_type(asset_type)

        items = []

        tokens = self._update_items(
            items,
            detail.supply_token_list,
            asset_type,
            token_role=TokenRole.SUPPLY,
            pool_id=pool_id,
        )
        self._update_items(
            items,
            detail.borrow_token_list,
            borrow_type,
            tokens,
            token_role=TokenRole.BORROW,
            pool_id=pool_id,
        )
        self._update_items(
            items,
            detail.reward_token_list,
            reward_type,
            tokens,
            token_role=TokenRole.REWARD,
            pool_id=pool_id,
        )
        self._update_items(items, detail.token_list, asset_type, pool_id=pool_id)

        pool = pools.get(pool_id)

        if pool is None:
            pool = Pool.from_api(
                pool_id=pool_id,
                protocol=pool_protocol,
                locked_until=locked_until,
                health_rate=health_rate,
                items=items,
                token_set=detail.description,
                project_id=item.pool.project_id if item.pool else None,
                adapter_id=item.pool.adapter_id if item.pool else None,
            )
        else:
            pool.append_items(items)

        return pool

    def _update_items(
        self,
        items: List[BalanceItem],
        raw_balances: list[dict],
        asset_type: AssetType,
        tokens: Optional[List[str]] = None,
        token_role: Optional[TokenRole] = None,
        pool_id: Optional[str] = None,
    ):
        if not raw_balances:
            return

        if tokens is None:
            tokens = sorted(
                list(
                    set(
                        [
                            self._balance_parser.get_symbol(DebankModelBalanceItem(**b))
                            for b in raw_balances
                        ]
                    )
                )
            )

        balances = self._balance_parser.parse(
            raw_balances,
            asset_type,
            False,
            token_set=tokens if len(raw_balances) > 1 else None,
            token_role=token_role,
            pool_id=pool_id,
        )

        items.extend(balances)
        return tokens

    @staticmethod
    def _get_pool_id(item: DebankModelPortfolioItem) -> str:
        return item.pool.id if item.pool else item.pool_id

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
        return REWARD_ASSET_TYPE_MAP.get(asset_type, asset_type)


class DebankApi(CustomizableBlockchainApi, IBalance, IPortfolio):
    """
    DeBank OpenApi: https://open.debank.com/
    """

    API_BASE_URL = 'https://pro-openapi.debank.com'
    API_BASE_RATE_LIMIT = 0.05  # 20 req / s

    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url=API_BASE_URL,
        rate_limit=API_BASE_RATE_LIMIT,
    )

    coin = None

    supported_requests = {
        'get_balance': '/v1/user/all_token_list?id={address}&is_all={is_all}',
        'get_portfolio': '/v1/user/all_complex_protocol_list?id={address}',
        'get_protocols': '/v1/protocol/all_list',
    }

    default_protocol_cache = DebankProtocolCache()

    def __init__(
        self,
        api_key: str,
        is_all: bool,
        protocol_cache: Optional[DebankProtocolCache] = None,
        base_url: Optional[str] = None,
    ):
        super().__init__(base_url)

        self._is_all = bool(is_all)
        self._headers = {'AccessKey': api_key}
        self._protocol_cache = protocol_cache or self.default_protocol_cache
        self._balance_parser = DebankBalanceParser(self._protocol_cache)
        self._protocol_parser = DebankProtocolParser()
        self._portfolio_parser = DebankPortfolioParser(
            self._protocol_parser, self._balance_parser
        )

    def get_balance(self, address: str) -> List[BalanceItem]:
        self._maybe_update_protocols()
        response = self.get(
            'get_balance', headers=self._headers, address=address, is_all=self._is_all
        )
        if self._has_error(response):
            return []

        return self._balance_parser.parse(response)

    def get_protocols(self) -> Dict[str, Protocol]:
        response = self.get('get_protocols', headers=self._headers)
        if self._has_error(response):
            return {}

        return self._protocol_parser.parse(response)

    def get_portfolio(self, address: str) -> List[Pool]:
        self._maybe_update_protocols()
        response = self.get('get_portfolio', headers=self._headers, address=address)
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
