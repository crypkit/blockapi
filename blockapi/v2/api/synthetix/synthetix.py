import logging
from abc import ABC
from decimal import Decimal
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from eth_typing import ChecksumAddress
from typing_extensions import TypedDict
from web3 import Web3

from blockapi.utils.num import raw_to_decimals, safe_decimal, to_decimal
from blockapi.v2.api.synthetix.synthetix_abi import (
    erc20_abi,
    exchangerates_abi,
    feepool_abi,
    rewards_escrow_v2_abi,
    staking_rewards_abi,
    synthetix_abi,
    system_settings_abi,
)
from blockapi.v2.api.web3_utils import (
    easy_call,
    ensure_checksum_address,
    get_eth_client,
)
from blockapi.v2.base import BlockchainApi, IBalance
from blockapi.v2.coins import COIN_SNX
from blockapi.v2.models import AssetType, BalanceItem, Blockchain, Coin

logger = logging.getLogger(__name__)


class CollateralizationStats(TypedDict):
    collateralization_ratio: Decimal
    collateralization_ratio_perc: Decimal


class StakingToken(TypedDict):
    symbol: str
    staked: Decimal
    rewards: Decimal


class WeeklyReward(TypedDict):
    exchange: Decimal
    staking: Decimal


class Rewards(TypedDict):
    prev_week: WeeklyReward
    this_week: WeeklyReward


class Staking(CollateralizationStats):
    transferable: Decimal
    debt: Decimal
    staked: Decimal
    vesting: Decimal
    collateral: Decimal
    rewards: Rewards
    staking_tokens: List[StakingToken]


class Synth(TypedDict):
    symbol: str
    contract_address: str


# noinspection PyBroadException
@lru_cache(maxsize=128)
def snx_contract_address(
    contract_name: str, network: str = "mainnet"
) -> ChecksumAddress:
    """
    Dynamically converts Synthetix contract name into its
    Ethereum address.
    """
    if network == 'optimism':
        return snx_optimism_contract_address(contract_name)

    base = "https://contracts.synthetix.io"
    url = (
        f"{base}/{contract_name}"
        if network == "mainnet"
        else f"{base}/{network}/{contract_name}"
    )

    result = requests.get(url)

    # contract address is obtained from redirected etherscan url,
    # as last 42 characters
    try:
        contract_address = result.url[-42:]
        return Web3.toChecksumAddress(contract_address)
    except Exception:
        raise ValueError(f'Contract {contract_name} not found.')


# noinspection PyBroadException
def snx_optimism_contract_address(
    contract_name: str,
) -> ChecksumAddress:
    """
    Dynamically converts Synthetix contract name into its
    Ethereum address on Optimism L2.
    """
    try:
        page = requests.get('https://docs.synthetix.io/addresses/')
        soup = BeautifulSoup(page.text, 'lxml')

        # find table with Mainnet Optimism contracts
        # https://docs.synthetix.io/addresses/#mainnet-optimism-l2
        header = soup.body.find('h2', {'id': 'mainnet-optimism-l2'})
        table = header.find_next(name='table')

        # find row where (any) cell's text equals contract_name
        row = table.find('td', text=contract_name).parent

        # our contract address is in 6th cell, raw row's content looks
        # like this:
        # `\n, name, \n, url to contract's source, \n, CONTRACT_ADDRESS, \n`
        # + remove all possible whitespaces and format address to checksum
        return Web3.toChecksumAddress(row.contents[5].text.strip())

    except Exception:
        raise ValueError(f'Contract {contract_name} not found.')


def get_staking_tokens(network: str) -> List[Tuple[str, str]]:
    """
    Get supported staking tokens for network.
    TODO add testnet networks.
    """
    # noinspection SpellCheckingInspection
    return (
        [
            ('iBTC', 'StakingRewardsiBTC'),
            ('iETH', 'StakingRewardsiETH'),
            ('sTSLA', 'StakingRewardssTSLABalancer'),
        ]
        if network == 'mainnet'
        else []
    )


class SynthetixApi(BlockchainApi, IBalance, ABC):
    decimals: Decimal = Decimal('18')
    coin = COIN_SNX

    def __init__(self, network: str, api_url: str):
        super().__init__()
        self.network = network
        self.blockchain = self.get_blockchain(self.network)
        self.w3 = get_eth_client(api_url)

    def get_balance(self, address: str) -> List[BalanceItem]:
        address = ensure_checksum_address(address)
        return list(self.yield_balances(address))

    def yield_balances(self, address) -> Iterable[BalanceItem]:
        """
        Fetch all balances for snx and synth tokens.
        """
        logger.info("Called Synthetix.yield_balances for address: %s", address)

        staking = self.fetch_staking(address)

        if staking['transferable']:
            yield self._create_balance(
                'SNX', AssetType.AVAILABLE, staking['transferable']
            )

        if staking['debt']:
            yield self._create_balance('sUSD', AssetType.DEBT, staking['debt'])

        if staking['staked']:
            yield self._create_balance('SNX', AssetType.STAKED, staking['staked'])

        if staking['vesting']:
            yield self._create_balance('SNX', AssetType.VESTING, staking['vesting'])

        rewards = Decimal("0")
        for token in staking.get('staking_tokens'):
            if token['staked']:
                yield self._create_balance(
                    token['symbol'], AssetType.STAKED, token['staked']
                )

            if token["rewards"]:
                rewards += token["rewards"]

        if rewards:
            yield self._create_balance('SNX', AssetType.CLAIMABLE, rewards)

    def _create_balance(
        self, symbol: str, asset_type: AssetType, balance_raw: Decimal
    ) -> BalanceItem:
        """
        Create balance item.
        """

        coin = self._get_coin(symbol)

        return BalanceItem(
            balance_raw=balance_raw,
            balance=balance_raw * pow(10, -self.decimals),
            coin=coin,
            asset_type=asset_type,
            raw={},
        )

    def _get_coin(self, symbol: str) -> Coin:
        return Coin(
            symbol=symbol,
            blockchain=self.blockchain,
            name=symbol,
            decimals=int(self.decimals),
            address=self._get_synth_contract(symbol),
        )

    @staticmethod
    def get_blockchain(network: str) -> Blockchain:
        return Blockchain.OPTIMISM if network == 'optimism' else Blockchain.ETHEREUM

    # noinspection PyTypeChecker
    def fetch_staking(self, address: str) -> Staking:
        """
        Fetch Synthetix staking info.
        """
        staking_tokens = get_staking_tokens(self.network)

        ratio = self.get_collateralization_ratio(address)
        return {
            **ratio,
            'transferable': self.get_snx_transferable_amount(address),
            'debt': self.get_total_debt_owed(address),
            'staked': self.compute_snx_staked_amount(address),
            'vesting': self.get_total_escrowed_amount(address),
            'collateral': self.get_collateral(address),
            'rewards': self.get_fees_and_rewards(address),
            'staking_tokens': list(
                self.yield_token_staking_data(address, staking_tokens)
            ),
        }

    def get_snx_transferable_amount(self, address: str) -> Decimal:
        """
        Returns total amount of unlocked SNX tokens.
        """
        snx_contract = self.w3.eth.contract(
            snx_contract_address('Synthetix', self.network), abi=synthetix_abi
        )
        amount = easy_call(snx_contract, 'transferableSynthetix', address)
        return to_decimal(amount)

    def get_total_debt_owed(self, address: str) -> Decimal:
        """
        Returns total debt owed in sUSD.
        """
        snx_contract = self.w3.eth.contract(
            snx_contract_address('Synthetix', self.network), abi=synthetix_abi
        )
        debt = easy_call(snx_contract, 'debtBalanceOf', address, b'sUSD')
        return to_decimal(debt)

    @lru_cache(maxsize=128)
    def get_collateralization_ratio(self, address) -> CollateralizationStats:
        """
        Returns collateralization ratio in %.
        """
        snx_contract = self.w3.eth.contract(
            snx_contract_address('Synthetix', self.network), abi=synthetix_abi
        )
        c_ratio = easy_call(snx_contract, 'collateralisationRatio', address)
        if c_ratio:
            ratio = raw_to_decimals(c_ratio, int(self.decimals))
            return {
                'collateralization_ratio': ratio,
                'collateralization_ratio_perc': 1 / ratio * 100,
            }
        else:
            return {
                'collateralization_ratio': Decimal("0"),
                'collateralization_ratio_perc': Decimal("0"),
            }

    @lru_cache(maxsize=512)
    def get_collateral(self, address: str) -> Decimal:
        """
        Return collateral.
        """
        snx_contract = self.w3.eth.contract(
            snx_contract_address('Synthetix', self.network), abi=synthetix_abi
        )
        collateral = easy_call(snx_contract, 'collateral', address)
        return to_decimal(collateral)

    def compute_snx_staked_amount(self, address: str) -> Decimal:
        """
        Return total staked snx amount.
        """
        system_contract = self.w3.eth.contract(
            snx_contract_address('SystemSettings', self.network),
            abi=system_settings_abi,
        )
        i_ratio = easy_call(system_contract, 'issuanceRatio')
        i_ratio = raw_to_decimals(i_ratio, int(self.decimals))

        collateral = self.get_collateral(address)
        collateralization_ratio = self.get_collateralization_ratio(address)[
            "collateralization_ratio"
        ]

        return collateral * min(Decimal("1"), collateralization_ratio / i_ratio)

    def get_fees_and_rewards(self, address: str) -> Rewards:
        """
        Returns the available Synth exchange rewards (fees, in sUSD) and
        SNX staking rewards (in SNX) as 3 tuples, current one (not yet
        claimable), one week ago, two weeks ago
        These values (except current ones) are zeroed as soon as
        the rewards are claimed!
        The current one is zeroed at the beginning of next fee period.
        """
        fee_pool_contract = self.w3.eth.contract(
            snx_contract_address('FeePool', self.network), abi=feepool_abi
        )
        fees = easy_call(fee_pool_contract, 'feesByPeriod', address)

        return {
            "prev_week": {
                "exchange": to_decimal(fees[1][0]),
                "staking": to_decimal(fees[1][1]),
            },
            "this_week": {
                "exchange": to_decimal(fees[0][0]),
                "staking": to_decimal(fees[0][1]),
            },
        }

    def yield_token_staking_data(
        self, address: str, synths: List[Tuple[str, str]]
    ) -> Iterable[StakingToken]:
        for symbol, contract_name in synths:
            staking_contract = self.w3.eth.contract(
                snx_contract_address(contract_name, self.network),
                abi=staking_rewards_abi,
            )

            staked = easy_call(staking_contract, 'balanceOf', address)
            rewards = easy_call(staking_contract, 'earned', address)
            yield {
                'symbol': symbol,
                'staked': to_decimal(staked),
                'rewards': to_decimal(rewards),
            }

    @lru_cache()
    def _get_synth_contract(self, symbol: str) -> str:
        """
        Get synth contract address.
        """
        snx_contract = self.w3.eth.contract(
            snx_contract_address('Synthetix', self.network), abi=synthetix_abi
        )

        if symbol == 'SNX':
            synth_addr = easy_call(snx_contract, 'proxy')
        else:
            synth_contract_addr = Web3.toChecksumAddress(
                easy_call(snx_contract, 'synths', symbol.encode())
            )
            synth_contract = self.w3.eth.contract(synth_contract_addr, abi=erc20_abi)
            synth_addr = easy_call(synth_contract, 'proxy')

        return synth_addr

    def get_total_escrowed_amount(self, address: str) -> Decimal:
        """
        Return number of SNX tokens escrowed.
        """
        rewards_escrow_contract = self.w3.eth.contract(
            snx_contract_address('RewardEscrowV2', self.network),
            abi=rewards_escrow_v2_abi,
        )
        total_escrowed = easy_call(
            rewards_escrow_contract,
            "totalEscrowedAccountBalance",
            address,
        )

        return to_decimal(total_escrowed)

    def get_token_xchg_rates(self, synths: List[Synth]) -> Dict:
        """
        Reads Synthetix tokens exchange rates needed for further
        calculations.
        """
        xchg_contract = self.w3.eth.contract(
            snx_contract_address('ExchangeRates', self.network),
            abi=exchangerates_abi,
        )
        xchg_rates = {}

        for synth in synths:
            symbol = (
                synth['symbol'][0].lower() + synth['symbol'][1:4]
                if len(synth['symbol']) >= 4
                else synth['symbol']
            )

            xchg_rates[synth['contract_address']] = raw_to_decimals(
                easy_call(
                    xchg_contract,
                    'rateForCurrency',
                    symbol.encode('utf-8'),
                ),
                decimals=int(self.decimals),
            )

        xchg_rates['XDR'] = safe_decimal(
            easy_call(xchg_contract, 'effectiveValue', b'XDR', 1, b'sUSD')
        )

        return xchg_rates


class SynthetixMainnetApi(SynthetixApi):
    def __init__(
        self,
        api_url: str,
    ):
        super().__init__(network="mainnet", api_url=api_url)


class SynthetixOptimismApi(SynthetixApi):
    def __init__(
        self,
        api_url: str,
    ):
        super().__init__(network='optimism', api_url=api_url)
