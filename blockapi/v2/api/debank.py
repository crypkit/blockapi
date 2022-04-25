import logging
from typing import Dict, List, Union, Optional
from eth_utils import to_checksum_address

from blockapi.v2.base import ApiOptions, BlockchainApi, IBalance
from blockapi.v2.models import BalanceItem, Blockchain, Coin, CoinInfo, Protocol

logger = logging.getLogger(__name__)


class DebankApi(BlockchainApi, IBalance):
    """
    DeBank OpenApi: https://openapi.debank.com/docs
    """

    API_BASE_URL = 'https://openapi.debank.com'
    API_BASE_RATE_LIMIT = 0.05  # 20 req / s

    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,  # ????
        base_url=API_BASE_URL,
        rate_limit=API_BASE_RATE_LIMIT,
    )

    @staticmethod
    def to_checksum_address(address: str) -> str:
        try:
            return to_checksum_address(address)
        except ValueError as e:
            logger.exception(e)
            return address

    supported_requests = {
        'get_balance': '/v1/user/token_list?id={address}&is_all=false',
        'get_protocols': '/v1/protocol/list'
    }

    def __init__(self):
        super().__init__()
        self._protocols = None

    def get_balance(self, address: str) -> [BalanceItem]:
        response = self.get('get_balance', address=address)
        return self._parse_items(response)

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

    def _parse_items(self, response: Union[List, Dict]) -> [BalanceItem]:
        if self._has_error(response):
            return []

        balances = []
        for raw_balance in response:
            balance = self._parse_raw_balance(raw_balance)
            if balance is not None:
                balances.append(balance)

        return balances

    def _fetch_protocols(self):
        response = self.get('get_protocols')
        protocols = {}
        for item in response:
            protocol = Protocol.from_api(
                protocol_id=item.get('id'),
                chain=item.get('chain'),
                name=item.get('name'),
                site_url=item.get('site_url'),
                logo_url=item.get('logo_url'),
                has_supported_portfolio=item.get('has_supported_portfolio', False)
            )
            protocols[protocol.protocol_id] = protocol

        self._protocols = protocols

    def _get_protocol(self, protocol_id):
        if protocol_id == '':
            return None

        if self._protocols is None:
            self._fetch_protocols()

        protocol = self._protocols.get(protocol_id)
        if protocol is None:
            logger.debug("Protocol '%s' not found.", protocol_id)

        return protocol

    def _parse_raw_balance(self, raw_balance: Dict) -> Optional[BalanceItem]:
        raw_amount = raw_balance.get('raw_amount', 0)
        if raw_amount == 0:
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
            address=self.to_checksum_address(raw_balance.get('id')),
            standards=[],
            info=CoinInfo(logo_url=raw_balance.get('logo_url')),
        )

        balance = BalanceItem.from_api(
            balance_raw=raw_amount,
            coin=coin,
            last_updated=raw_balance.get('time_at'),
            raw=raw_balance,
            protocol=self._get_protocol(raw_balance.get('protocol_id', ''))
        )

        return balance

    def __repr__(self):
        return f"{self.__class__.__name__}"
