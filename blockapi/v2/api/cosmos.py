import json
from abc import ABCMeta
from typing import Dict, Iterable, Optional

from requests import Response

from blockapi.v2.base import (
    ApiException,
    ApiOptions,
    BlockchainApi,
    IBalance,
    InvalidAddressException,
)
from blockapi.v2.coins import COIN_ATOM
from blockapi.v2.models import BalanceItem, Blockchain, Coin, CoinInfo


class CosmosBaseAPI(BlockchainApi, IBalance, metaclass=ABCMeta):
    """
    Cosmos RPC
    API docs: https://cosmos.network/rpc/
    Explorer: https://www.mintscan.io
    """

    API_BASE_URL = 'https://api.covalenthq.com/v1'
    API_BASE_RATE_LIMIT = 0.2

    supported_requests = {
        'get_balances': '/cosmos/bank/v1beta1/balances/{address}',
    }

    def get_balance(self, address: str) -> list[BalanceItem]:
        response = self.get('get_balances', address=address)

        balances = []
        for b in response['balances']:
            if b['denom'] != self.coin.address:
                # add token loading
                continue

            balances.append(
                BalanceItem.from_api(balance_raw=b['available'], coin=self.coin, raw=b)
            )

        return balances


class CosmosAPI(CosmosBaseAPI):
    coin = COIN_ATOM
    api_options = ApiOptions(
        blockchain=Blockchain.ARBITRUM,
        base_url=CosmosBaseAPI.API_BASE_URL,
        rate_limit=CosmosBaseAPI.API_BASE_RATE_LIMIT,
    )
