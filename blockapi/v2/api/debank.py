import logging
from datetime import datetime, timedelta
from decimal import Decimal
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Union

import attr
from pydantic import BaseModel, validator

from blockapi.utils.address import make_checksum_address
from blockapi.utils.datetime import parse_dt
from blockapi.utils.num import decimals_to_raw
from blockapi.v2.api.debank_maps import (
    COINGECKO_IDS_BY_CONTRACTS,
    DEBANK_ASSET_TYPES,
    NATIVE_COIN_MAP,
    REWARD_ASSET_TYPE_MAP,
)
from blockapi.v2.base import (
    ApiOptions,
    BalanceMixin,
    CustomizableBlockchainApi,
    IPortfolio,
)
from blockapi.v2.blockchain_mapping import get_blockchain_from_debank_chain
from blockapi.v2.models import (
    AssetType,
    BalanceItem,
    Blockchain,
    Coin,
    CoingeckoId,
    CoinInfo,
    FetchResult,
    ParseResult,
    Pool,
    PoolInfo,
    Protocol,
)

logger = logging.getLogger(__name__)

MIST_SYMBOL = 'MIST'


class DebankModelBalanceItem(BaseModel):
    id: str
    chain: str
    name: str
    symbol: str
    display_symbol: Optional[str] = None
    optimized_symbol: Optional[str] = None
    decimals: int
    logo_url: Optional[str] = None
    protocol_id: Optional[str] = None
    time_at: Optional[float] = None
    amount: float
    raw_amount: Optional[float] = None
    raw_value: Optional[dict] = None


class DebankModelPoolItemDetail(BaseModel):
    description: Optional[str] = None
    health_rate: Optional[float] = None
    unlock_at: Optional[float] = None
    token_list: Optional[list[dict]] = None
    supply_token_list: Optional[list[dict]] = None
    borrow_token_list: Optional[list[dict]] = None
    reward_token_list: Optional[list[dict]] = None


class DebankModelPoolItem(BaseModel):
    id: str
    project_id: str
    adapter_id: Optional[str]
    controller: Optional[str]


class DebankModelPortfolioItem(BaseModel):
    name: str
    detail: DebankModelPoolItemDetail
    pool_id: Optional[str] = None
    pool: Optional[DebankModelPoolItem] = None
    position_index: Optional[str] = None

    @validator('pool')
    def require_pool_or_pool_id(cls, v, values, **kwargs):
        if v is not None:
            return v

        if 'pool_id' not in values or values['pool_id'] is None:
            raise ValueError('either pool or pool_id must have a value')

        return v


@attr.s(auto_attribs=True, slots=True, frozen=True)
class DebankUsageStats:
    usage: Decimal
    remains: Decimal
    date: datetime

    @classmethod
    def from_api(
        cls,
        *,
        usage: Union[str, float, int],
        remains: Union[str, float, int],
        date: str,
    ) -> 'DebankUsageStats':
        return cls(usage=Decimal(usage), remains=Decimal(remains), date=parse_dt(date))


@attr.s(auto_attribs=True, slots=True, frozen=True)
class DebankUsage:
    balance: Decimal
    stats: list[DebankUsageStats]

    @classmethod
    def from_api(
        cls, *, balance: Union[str, float, int], stats: List[DebankUsageStats]
    ) -> 'DebankUsage':
        return cls(balance=Decimal(balance), stats=stats)


class DebankModelProtocol(BaseModel):
    id: str
    chain: str
    name: str
    site_url: Optional[str]
    logo_url: Optional[str]
    has_supported_portfolio: Optional[bool] = False
    tvl: Optional[float]


class DebankModelPortfolio(DebankModelProtocol):
    portfolio_item_list: list[DebankModelPortfolioItem]


class DebankModelChain(BaseModel):
    id: str
    community_id: int
    name: str
    native_token_id: str
    logo_url: str
    wrapped_token_id: str
    is_support_pre_exec: bool


class DebankChain(BaseModel):
    chain: Blockchain
    community_id: int
    name: str
    logo_url: str


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
            logger.warning(f'No blockchain found for protocol {item.id}. Skipping.')
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


class DebankChainParser:
    def parse(self, response: List) -> list[DebankChain]:
        chains = []
        for item in response:
            model = DebankModelChain.parse_obj(item)
            if chain := self.parse_item(model):
                chains.append(chain)

        return list(sorted(chains, key=lambda x: x.name))

    @staticmethod
    def parse_item(item: DebankModelChain) -> Optional[DebankChain]:
        blockchain = get_blockchain_from_debank_chain(item.id)
        if not blockchain:
            logger.warning(
                f'No blockchain found for debank chain {item.id} ({item.name}, {item.community_id}). Skipping.'
            )
            return None

        return DebankChain(
            chain=blockchain,
            community_id=item.community_id,
            name=item.name,
            logo_url=item.logo_url,
        )


class DebankUsageParser:
    def parse(self, response: dict) -> DebankUsage:
        return DebankUsage.from_api(
            balance=response.get('balance'),
            stats=[self._parse_stats(u) for u in response.get('stats', [])],
        )

    @staticmethod
    def _parse_stats(response) -> DebankUsageStats:
        return DebankUsageStats.from_api(
            usage=response.get('usage'),
            remains=response.get('remains'),
            date=response.get('date'),
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


@lru_cache
def get_coingecko_id(contract, symbol) -> Optional[CoingeckoId]:
    return next(
        (
            it.coingecko_id
            for it in COINGECKO_IDS_BY_CONTRACTS
            if it.symbol == symbol and contract in it.contracts
        ),
        None,
    )


class DebankBalanceParser:
    def __init__(self, protocol_cache: DebankProtocolCache):
        self._protocols = protocol_cache

    def parse(
        self,
        response: Union[list, dict],
        asset_type: AssetType = AssetType.AVAILABLE,
        is_wallet: bool = True,
        pool_info: Optional[PoolInfo] = None,
    ) -> List[BalanceItem]:
        if not response:
            return []

        items = []
        for item in response:
            balance_item = DebankModelBalanceItem(**item)
            balance_item.raw_value = item

            balance = self.parse_item(balance_item, asset_type, is_wallet, pool_info)
            if balance is not None:
                items.append(balance)

        return items

    def parse_item(
        self,
        balance_item: DebankModelBalanceItem,
        asset_type: AssetType = AssetType.AVAILABLE,
        is_wallet: bool = True,
        pool_info: Optional[PoolInfo] = None,
    ) -> Optional[BalanceItem]:
        raw_amount = balance_item.raw_amount or 0
        amount = balance_item.amount or 0

        if raw_amount == 0 and amount == 0:
            logger.debug(
                "Skipping balance item: '%s' - balance is zero.",
                balance_item.name,
            )

            return None

        coin = self.get_coin(balance_item)

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

        protocol = self._protocols.get(balance_item.protocol_id)

        balance = BalanceItem.from_api(
            balance_raw=raw_amount,
            coin=coin,
            asset_type=asset_type,
            last_updated=balance_item.time_at,
            raw=balance_item.raw_value,
            protocol=protocol,
            is_wallet=is_wallet,
            pool_info=pool_info,
        )

        return balance

    def get_coin(self, balance_item: DebankModelBalanceItem) -> Coin:
        contract = balance_item.id
        blockchain = get_blockchain_from_debank_chain(balance_item.chain)
        symbol = self.get_symbol(balance_item)

        coingecko_id = get_coingecko_id(contract, symbol)

        coin = NATIVE_COIN_MAP.get((blockchain, coingecko_id))
        if coin and coin.protocol_id == balance_item.protocol_id:
            return coin

        check_address = make_checksum_address(contract)
        if check_address:
            contract = check_address

        return Coin.from_api(
            symbol=symbol,
            name=balance_item.name,
            decimals=balance_item.decimals,
            blockchain=blockchain,
            address=contract,
            standards=[],
            protocol_id=balance_item.protocol_id,
            info=CoinInfo(logo_url=balance_item.logo_url, coingecko_id=coingecko_id),
        )

    @staticmethod
    def get_symbol(raw_balance: DebankModelBalanceItem) -> str:
        if raw_balance.optimized_symbol == MIST_SYMBOL:
            return MIST_SYMBOL

        return (
            raw_balance.symbol
            or raw_balance.optimized_symbol
            or raw_balance.display_symbol
        )

    @staticmethod
    def _get_native_coin(
        blockchain: Blockchain, address: str, symbol: str
    ) -> Optional[Coin]:
        if coin is not None and coin.blockchain == blockchain:
            return coin


class DebankPortfolioParser:
    def __init__(
        self, protocol_parser: DebankProtocolParser, balance_parser: DebankBalanceParser
    ):
        self._protocol_parser = protocol_parser
        self._balance_parser = balance_parser

    def parse(self, response: Union[list, dict]) -> list[Pool]:
        items = []
        if response:
            for item in response:
                portfolio = DebankModelPortfolio(**item)
                parsed = self.parse_items(portfolio)
                items.extend(parsed)

        return items

    def parse_items(self, raw_portfolio: DebankModelPortfolio) -> List[Pool]:
        root_protocol = self._protocol_parser.parse_item(raw_portfolio)
        if not root_protocol:
            return []

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
            pool_info = pool.pool_info
            if pool_info.pool_id:
                pools[(pool_info.pool_id, pool_info.position_index)] = pool

            items.append(pool)

        return items

    def _parse_portfolio_item(
        self,
        item: DebankModelPortfolioItem,
        pool_protocol: Protocol,
        pools: Dict[tuple[str, str], Pool],
    ) -> Pool:
        pool_id = self._get_pool_id(item)
        detail = item.detail

        health_rate = detail.health_rate
        locked_until = detail.unlock_at
        position_index = item.position_index

        pool = pools.get((pool_id, position_index))

        if pool is None:
            tokens = (
                self._get_tokens(detail.supply_token_list)
                if detail.supply_token_list
                else []
            )

            pool_info = PoolInfo.from_api(
                pool_id=pool_id,
                project_id=item.pool.project_id if item.pool else pool_id,
                name=detail.description if detail.description else None,
                adapter_id=item.pool.adapter_id if item.pool else None,
                controller=item.pool.controller if item.pool else None,
                position_index=position_index,
                tokens=tokens,
            )

            pool = Pool.from_api(
                pool_info=pool_info,
                protocol=pool_protocol,
                locked_until=locked_until,
                health_rate=health_rate,
                items=[],
            )

        items = list(self._parse_balances(detail, item, pool.pool_info))
        pool.append_items(items)

        return pool

    def _parse_balances(self, detail, item, pool_info) -> Iterable[BalanceItem]:
        asset_type = self._parse_asset_type(item.name)
        borrow_type = self._get_borrow_asset_type(asset_type)
        reward_type = self._get_reward_asset_type(asset_type)

        yield from self._parse_token_list(
            detail.supply_token_list,
            asset_type,
            pool_info=pool_info,
        )

        yield from self._parse_token_list(
            detail.borrow_token_list,
            borrow_type,
            pool_info=pool_info,
        )

        yield from self._parse_token_list(
            detail.reward_token_list,
            reward_type,
            pool_info=pool_info,
        )

        yield from self._parse_token_list(
            detail.token_list, asset_type, pool_info=pool_info
        )

    def _get_tokens(self, raw_balances: list[dict]):
        symbols = [
            self._balance_parser.get_symbol(DebankModelBalanceItem(**b))
            for b in raw_balances
        ]

        return sorted(symbols)

    def _parse_token_list(
        self,
        raw_balances: list[dict],
        asset_type: AssetType,
        pool_info: Optional[PoolInfo] = None,
    ) -> Iterable[BalanceItem]:
        if not raw_balances:
            return

        yield from self._balance_parser.parse(
            raw_balances,
            asset_type,
            False,
            pool_info=pool_info,
        )

    @staticmethod
    def _get_pool_id(item: DebankModelPortfolioItem) -> str:
        return item.pool.id if item.pool else item.pool_id

    @staticmethod
    def _parse_asset_type(type_: str) -> Optional[AssetType]:
        # list of valid types: https://docs.open.debank.com/en/reference/api-models/portfolioitemobject
        if type_ is None:
            return AssetType.LOCKED

        try:
            lower = type_.lower()
            asset_type = DEBANK_ASSET_TYPES.get(lower)
            if asset_type:
                return asset_type

            return AssetType(lower)
        except ValueError as ve:
            logger.error(ve)
            return AssetType.LOCKED

    @staticmethod
    def _get_borrow_asset_type(asset_type):
        if asset_type == AssetType.LENDING:
            return AssetType.LENDING_BORROW

        return asset_type

    @staticmethod
    def _get_reward_asset_type(asset_type):
        return REWARD_ASSET_TYPE_MAP.get(asset_type, asset_type)


class DebankApi(CustomizableBlockchainApi, BalanceMixin, IPortfolio):
    """
    DeBank OpenApi: https://open.debank.com/
    """

    API_BASE_RATE_LIMIT = 0.05  # 20 req / s

    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url='https://pro-openapi.debank.com',
        rate_limit=API_BASE_RATE_LIMIT,
    )

    coin = None

    supported_requests = {
        'get_balance': '/v1/user/all_token_list?id={address}&is_all={is_all}',
        'get_chains': '/v1/chain/list',
        'get_portfolio': '/v1/user/all_complex_protocol_list?id={address}',
        'get_protocols': '/v1/protocol/all_list',
        'usage': '/v1/account/units',
    }

    default_protocol_cache = DebankProtocolCache()

    def __init__(
        self,
        api_key: str,
        is_all: bool,
        protocol_cache: Optional[DebankProtocolCache] = None,
        base_url: Optional[str] = None,
    ):
        super().__init__(base_url=base_url)

        self._is_all = bool(is_all)
        self._headers = {'AccessKey': api_key}
        self._protocol_cache = protocol_cache or self.default_protocol_cache
        self._balance_parser = DebankBalanceParser(self._protocol_cache)
        self._protocol_parser = DebankProtocolParser()
        self._chain_parser = DebankChainParser()
        self._portfolio_parser = DebankPortfolioParser(
            self._protocol_parser, self._balance_parser
        )
        self._usage_parser = DebankUsageParser()

    def fetch_balances(self, address: str) -> FetchResult:
        return self.get_data(
            'get_balance',
            headers=self._headers,
            address=address,
            is_all=self._is_all,
        )

    def fetch_pools(self, address: str) -> FetchResult:
        return self.get_data(
            'get_portfolio',
            headers=self._headers,
            address=address,
        )

    def fetch_protocols(self) -> FetchResult:
        return self.get_data(
            'get_protocols',
            headers=self._headers,
        )

    def fetch_chains(self) -> FetchResult:
        return self.get_data(
            'get_chains',
            headers=self._headers,
        )

    def parse_balances(self, fetch_result: FetchResult) -> ParseResult:
        if error := self._get_error(fetch_result.data):
            return ParseResult(errors=[error])

        self._maybe_update_protocols()
        return ParseResult(data=self._balance_parser.parse(fetch_result.data))

    def parse_pools(self, fetch_result: FetchResult) -> ParseResult:
        if error := self._get_error(fetch_result.data):
            return ParseResult(errors=[error])

        self._maybe_update_protocols()
        return ParseResult(data=self._portfolio_parser.parse(fetch_result.data))

    def get_protocols(self) -> Dict[str, Protocol]:
        response = self.get('get_protocols', headers=self._headers)
        if self._has_error(response):
            return {}

        return self._protocol_parser.parse(response)

    def get_chains(self) -> list[DebankChain]:
        response = self.get('get_chains', headers=self._headers)
        if self._has_error(response):
            return []

        return self._chain_parser.parse(response)

    def get_portfolio(self, address: str) -> List[Pool]:
        self._maybe_update_protocols()
        response = self.get('get_portfolio', headers=self._headers, address=address)
        if self._has_error(response):
            return []

        return self._portfolio_parser.parse(response)

    def get_usage(self) -> Optional[DebankUsage]:
        response = self.get('usage', headers=self._headers)
        if self._has_error(response):
            return None

        return self._usage_parser.parse(response)

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

    @staticmethod
    def _get_error(data: Union[list, dict]) -> Optional[dict]:
        if not isinstance(data, dict):
            return None

        error = data.get('errors')
        message = data.get('message')

        if not error and not message:
            return None

        return dict(error=error, message=message)

    def __repr__(self):
        return f"{self.__class__.__name__}"
