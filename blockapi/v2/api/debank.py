from datetime import datetime, timedelta
import logging
from typing import Dict, List, Union, Optional
from eth_utils import to_checksum_address

from blockapi.utils.num import decimals_to_raw
from blockapi.v2.base import ApiOptions, BlockchainApi, IBalance, IPortfolio
from blockapi.v2.models import BalanceItem, Blockchain, Coin, CoinInfo, Protocol, PortfolioItem, Portfolio, DetailType

logger = logging.getLogger(__name__)


class DebankProtocolParser:
    def parse(self, response: List) -> Dict[str, Protocol]:
        protocols = {}
        for item in response:
            protocol = self.parse_item(item)
            protocols[protocol.protocol_id] = protocol

        return protocols

    def parse_item(self, item):
        return Protocol.from_api(
            protocol_id=item.get('id'),
            chain=item.get('chain'),
            name=item.get('name'),
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

    def parse(self, response: List) -> List[BalanceItem]:
        items = []
        for item in response:
            balance = self.parse_item(item)
            if balance is not None:
                items.append(balance)

        return items

    def parse_item(self, raw_balance: dict) -> Optional[BalanceItem]:
        raw_amount = raw_balance.get('raw_amount', 0)
        amount = raw_balance.get('amount', 0)

        if raw_amount == 0 and amount == 0:
            logger.debug(
                "Skipping coin: '%s' - balance is zero.",
                raw_balance.get("name"),
            )

            return None

        coin = Coin.from_api(
            symbol=raw_balance.get('symbol'),
            name=raw_balance.get('name'),
            decimals=raw_balance.get('decimals', 0),
            blockchain=raw_balance.get('chain'),
            address=make_checksum_address(raw_balance.get('id')),
            standards=[],
            info=CoinInfo(logo_url=raw_balance.get('logo_url')),
        )

        if raw_amount == 0 and amount != 0:
            raw_amount = decimals_to_raw(amount, coin.decimals)

        balance = BalanceItem.from_api(
            balance_raw=raw_amount,
            coin=coin,
            last_updated=raw_balance.get('time_at'),
            raw=raw_balance,
            protocol=self._protocols.get(raw_balance.get('protocol_id', '')),
        )

        return balance


def make_checksum_address(address: str) -> str:
    try:
        return to_checksum_address(address)
    except ValueError as e:
        logger.exception(e)
        return address


class DebankPortfolioParser:
    def __init__(self, protocol_parser: DebankProtocolParser, balance_parser: DebankBalanceParser):
        self._protocol_parser = protocol_parser
        self._balance_parser = balance_parser

    def parse(self, response: List) -> List[Portfolio]:
        items = []
        for item in response:
            parsed = self.parse_item(item)
            items.append(parsed)

        return items

    def parse_item(self, raw_portfolio) -> Portfolio:
        protocol = self._protocol_parser.parse_item(raw_portfolio)
        items = self._parse_portfolio_item_list(raw_portfolio.get('portfolio_item_list', []))

        return Portfolio.from_api(
            protocol=protocol,
            items=items,
        )

    def _parse_portfolio_item_list(self, raw_portfolio_items: List[Dict]) -> List[PortfolioItem]:
        items = []
        for item in raw_portfolio_items:
            parsed = self._parse_portfolio_item(item)
            items.append(parsed)

        return items

    def _parse_portfolio_item(self, item: Dict) -> PortfolioItem:
        detail = item.get('detail', {})
        supply_token_list = self._balance_parser.parse(detail.get('supply_token_list', []))
        borrow_token_list = self._balance_parser.parse(detail.get('borrow_token_list', []))
        token_list = self._balance_parser.parse(detail.get('token_list', []))

        pool_id_raw = item.get('pool_id')
        pool_id = make_checksum_address(pool_id_raw) if pool_id_raw is not None else None

        return PortfolioItem.from_api(
            name=item.get('name'),
            detail_types=self._parse_detail_types(item.get('detail_types', [])),
            last_updated=item.get('update_at'),
            pool_id=pool_id,
            supply_token_list=supply_token_list,
            borrow_token_list=borrow_token_list,
            token_list=token_list,
            raw_portfolio=item
        )

    def _parse_detail_types(self, types: List[str]) -> List[DetailType]:
        detail_types = []
        for type_ in types:
            try:
                detail_types.append(DetailType(type_))
            except ValueError as ve:
                logger.error(ve)

        return detail_types


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
        'get_balance': '/v1/user/token_list?id={address}&is_all=false',
        'get_portfolio': '/v1/user/complex_protocol_list?id={address}',
        'get_protocols': '/v1/protocol/list',
    }

    default_protocol_cache = DebankProtocolCache()

    def __init__(self, protocol_cache: Optional[DebankProtocolCache] = None):
        super().__init__()

        self._protocol_cache = protocol_cache or self.default_protocol_cache
        self._balance_parser = DebankBalanceParser(self._protocol_cache)
        self._protocol_parser = DebankProtocolParser()
        self._portfolio_parser = DebankPortfolioParser(self._protocol_parser, self._balance_parser)

    def get_balance(self, address: str) -> [BalanceItem]:
        self._maybe_update_protocols()
        response = self.get('get_balance', address=address)
        if self._has_error(response):
            return []

        return self._balance_parser.parse(response)

    def get_protocols(self) -> Dict[str, Protocol]:
        response = self.get('get_protocols')
        if self._has_error(response):
            return {}

        return self._protocol_parser.parse(response)

    def get_portfolio(self, address: str) -> List[Portfolio]:
        response = self.get('get_portfolio')
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
            logger.error(message)

        if error is not None:
            err_id = error.get('id')
            if err_id is not None:
                logger.error(err_id)

        return message is not None or error is not None

    def __repr__(self):
        return f"{self.__class__.__name__}"