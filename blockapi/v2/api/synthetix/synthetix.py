import logging
from abc import ABC
from decimal import Decimal
from functools import lru_cache
from typing import Dict, Iterable, List

import requests
from bs4 import BeautifulSoup
from eth_typing import ChecksumAddress
from marko import Markdown
from marko.block import Heading, HTMLBlock
from typing_extensions import TypedDict
from web3 import Web3

from blockapi.utils.num import raw_to_decimals, safe_decimal, to_decimal
from blockapi.v2.api.synthetix.synthetix_abi import (
    erc20_abi,
    exchangerates_abi,
    feepool_abi,
    liquidator_rewards_abi,
    rewards_escrow_v2_abi,
    synthetix_abi,
    system_settings_abi,
)
from blockapi.v2.api.web3_utils import (
    easy_call,
    ensure_checksum_address,
    get_eth_client,
)
from blockapi.v2.base import CustomizableBlockchainApi, IBalance
from blockapi.v2.coins import COIN_SNX
from blockapi.v2.models import ApiOptions, AssetType, BalanceItem, Blockchain, Coin

logger = logging.getLogger(__name__)


class CollateralizationStats(TypedDict):
    collateralization_ratio: Decimal
    collateralization_ratio_perc: Decimal


class WeeklyReward(TypedDict):
    exchange: Decimal
    staking: Decimal


class Staking(CollateralizationStats):
    transferable: Decimal
    debt: Decimal
    staked: Decimal
    vesting: Decimal
    collateral: Decimal
    rewards: WeeklyReward
    liquidation_reward: Decimal


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
        response = requests.get(
            'https://raw.githubusercontent.com/Synthetixio/synthetix-docs/master/content/addresses.md'
        )
        md = Markdown().parse(response.text)

        # find table with Optimism contracts
        html_tab_raw = None
        return_table = False
        for child in md.children:
            if return_table and type(child) is HTMLBlock:
                html_tab_raw = child.children
                break
            elif (
                type(child) is Heading
                and child.children[0].children == 'MAINNET Optimism (L2)'
            ):
                return_table = True

        table = BeautifulSoup(html_tab_raw, 'lxml')
        row = table.find('td', text=contract_name).parent
        return Web3.toChecksumAddress(row.contents[5].text.strip())

    except Exception:
        raise ValueError(f'Contract {contract_name} not found.')


class SynthetixApi(CustomizableBlockchainApi, IBalance, ABC):
    decimals: Decimal = Decimal('18')
    coin = COIN_SNX

    def __init__(self, network: str, api_url: str):
        super().__init__(base_url=api_url)
        self.network = network
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
        return self.yield_balances_from_staking(staking=staking)

    def yield_balances_from_staking(self, staking: Staking) -> Iterable[BalanceItem]:
        if staking['transferable']:
            yield self._create_balance(
                'SNX',
                AssetType.AVAILABLE,
                staking['transferable'],
                is_wallet=True,
            )

        if staking['debt']:
            yield self._create_balance('sUSD', AssetType.DEBT, staking['debt'])

        if staking['collateral']:
            stake_balance = (
                staking['collateral']
                - staking['vesting']
                - staking['liquidation_reward']
            )

            yield self._create_balance('SNX', AssetType.STAKED, stake_balance)

        if staking['vesting']:
            yield self._create_balance(
                'SNX', AssetType.PRICED_VESTING, staking['vesting']
            )

        if staking['rewards']['exchange']:
            yield self._create_balance(
                'sUSD', AssetType.REWARDS, staking['rewards']['exchange']
            )

        if staking['rewards']['staking']:
            yield self._create_balance(
                'SNX', AssetType.REWARDS, staking['rewards']['staking']
            )

        if staking['liquidation_reward']:
            yield self._create_balance(
                'SNX', AssetType.LIQUIDATION_REWARDS, staking['liquidation_reward']
            )

    def _create_balance(
        self,
        symbol: str,
        asset_type: AssetType,
        balance_raw: Decimal,
        is_wallet: bool = False,
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
            is_wallet=is_wallet,
            raw={},
        )

    def _get_coin(self, symbol: str) -> Coin:
        return Coin(
            symbol=symbol,
            blockchain=self.api_options.blockchain,
            name=symbol,
            decimals=int(self.decimals),
            address=self._get_synth_contract(symbol),
        )

    # noinspection PyTypeChecker
    def fetch_staking(self, address: str) -> Staking:
        """
        Fetch Synthetix staking info.
        """
        ratio = self.get_collateralization_ratio(address)

        return {
            **ratio,
            'transferable': self.get_snx_transferable_amount(address),
            'debt': self.get_total_debt_owed(address),
            'staked': self.compute_snx_staked_amount(address),
            'vesting': self.get_total_escrowed_amount(address),
            'collateral': self.get_collateral(address),
            'rewards': self.get_fees_and_rewards(address),
            'liquidation_reward': self.get_liquidation_reward(address),
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

    def get_fees_and_rewards(self, address: str) -> WeeklyReward:
        """
        Returns the available Synth exchange rewards (fees, in sUSD)
        and SNX staking rewards (in SNX) as tuple.
        """
        fee_pool_contract = self.w3.eth.contract(
            snx_contract_address('FeePool', self.network), abi=feepool_abi
        )
        fees = easy_call(fee_pool_contract, 'feesAvailable', address)

        return {"exchange": to_decimal(fees[0]), "staking": to_decimal(fees[1])}

    def get_liquidation_reward(self, address: str) -> Decimal:
        """
        Returns liquidation reward.
        """
        liq_rewards_contract = self.w3.eth.contract(
            snx_contract_address('LiquidatorRewards', self.network),
            abi=liquidator_rewards_abi,
        )
        fee = easy_call(liq_rewards_contract, 'earned', address)

        return to_decimal(fee)

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
    api_options = ApiOptions(blockchain=Blockchain.ETHEREUM, base_url=None)

    def __init__(
        self,
        api_url: str,
    ):
        super().__init__(network="mainnet", api_url=api_url)


class SynthetixOptimismApi(SynthetixApi):
    api_options = ApiOptions(blockchain=Blockchain.OPTIMISM, base_url=None)

    def __init__(
        self,
        api_url: str,
    ):
        super().__init__(network='optimism', api_url=api_url)
