from datetime import datetime
from decimal import Decimal
from functools import lru_cache
from logging import getLogger
from typing import Callable, Dict, Iterable, List, Optional, Tuple

import requests
from eth_typing import ChecksumAddress
from typing_extensions import TypedDict
from web3 import Web3

from blockapi.utils.num import safe_opt_decimal
from blockapi.v2.api.perpetual.perp_abi import rewards_abi
from blockapi.v2.api.web3_utils import easy_call, get_eth_client
from blockapi.v2.base import ApiOptions, BlockchainApi, IBalance
from blockapi.v2.coins import COIN_PERP
from blockapi.v2.models import AssetType, BalanceItem, Blockchain, Coin

logger = getLogger(__name__)


def perp_contract_address(contract_name: str) -> ChecksumAddress:
    """
    Get PERP contract address by name.
    """
    l1 = perp_contracts()['layers']['layer1']
    l1_c = l1['contracts']

    contract_map = {
        'PERP': l1['externalContracts']['perp'],
        'sPERP': l1_c['StakedPerpToken']['address'],
        'staking_rewards': l1_c['PerpStakingRewardNoVesting']['address'],
        'vesting_rewards': l1_c['PerpStakingRewardVesting']['address'],
    }

    if contract_name not in contract_map:
        raise ValueError('Invalid contract name.')

    contract_address = contract_map[contract_name]
    return Web3.toChecksumAddress(contract_address)


@lru_cache()
def perp_contracts() -> dict:
    response = requests.get('https://metadata.perp.exchange/production.json')
    return response.json()


class PerpSnapshot(TypedDict):
    epoch: int
    weekStart: str
    weekEnd: str
    redeemableUntil: int
    totalRewardPerp: str
    hash: str


class PerpReward(TypedDict):
    totalRewardPerp: str
    areaFactor: str


class PerpOffChainStorage:
    """
    Perp Off-chain storage for staking rewards, ... .
    """

    base_url = 'https://s3.amazonaws.com/staking.perp.fi/production'
    snapshot_urls = {
        'immediate': '/snapshot-immediate.json',
        'vesting': '/snapshot-vesting.json',
    }
    epoch_rewards_link = '/{epoch}/{hash}.json'

    @classmethod
    def get_epoch_snapshots(cls, snapshot_type: str) -> List[PerpSnapshot]:
        """
        Load epoch (weekly) immediate or vesting snapshots.
        """
        url = f"{cls.base_url}{cls.snapshot_urls[snapshot_type]}"
        response = requests.get(url)
        snapshots = response.json()

        for epoch, snapshot in snapshots.items():
            snapshot.update({'epoch': int(epoch)})

        return sorted(snapshots.values(), key=lambda i: i['epoch'])

    @classmethod
    @lru_cache(maxsize=128)
    def get_rewards(cls, epoch: int, hash_: str) -> Dict[str, PerpReward]:
        """
        Load perp rewards for whole epoch.
        """
        url = (
            f'{cls.base_url}'
            f'{cls.epoch_rewards_link.format(epoch=epoch, hash=hash_)}'
        )

        result = requests.get(url)

        try:
            return result.json()
        except requests.JSONDecodeError as e:
            logger.error(f"Request parsing to json failed: %s", result.text)
            raise e


class PerpProtocol:
    """
    Documentation how to get rewards and vesting.
    https://docs.google.com/document/d/1E2k8Ad2POodLWWyeklif0tx0-CVy_41_ONAS8n9RN68/edit
    """

    reward_contract = '0xc2a9e84D77f4B534F049b593C282c5c91F24808A'
    vesting_contract = '0x49a4B8431Fc24BE4b22Fb07D1683E2c52bC56088'

    def __init__(self, address, provider="infura"):
        self.address = address
        self.w3 = get_eth_client('mainnet', provider)

    def yield_balances(self) -> Iterable[BalanceItem]:
        """
        Fetch all balances for snx and synth tokens.
        """
        s_claimable = self._fetch_staking_claimable_rewards()
        v_claimable, v_locked = self._fetch_staking_vesting_rewards()
        claimable = s_claimable + v_claimable

        if claimable > Decimal(0):
            yield self._create_balance(AssetType.CLAIMABLE, claimable)

        if v_locked:
            yield self._create_balance(AssetType.VESTING, v_locked)

    def fetch_balances(self) -> List[BalanceItem]:
        return list(self.yield_balances())

    @staticmethod
    def _create_balance(asset_type: AssetType, amount: Decimal) -> BalanceItem:
        return BalanceItem.from_api(
            balance_raw=amount,
            coin=COIN_PERP,
            asset_type=asset_type,
            protocol='perpetual',
            raw={},
        )

    def _fetch_staking_claimable_rewards(self) -> Decimal:
        """
        Fetch claimable staking rewards.
        """
        snapshots = self._fetch_non_claimed_snapshots('immediate', 'staking_rewards')
        return self._get_total_reward(snapshots)

    def _fetch_staking_vesting_rewards(self) -> Tuple[Decimal, Decimal]:
        """
        Fetch staking vesting rewards, both claimable and locked.
        """
        snapshots = self._fetch_non_claimed_snapshots('vesting', 'vesting_rewards')

        current_ts = datetime.utcnow().timestamp()

        claimable = self._get_total_reward(
            snapshots, lambda s: current_ts > s['redeemableUntil']
        )
        locked = self._get_total_reward(
            snapshots, lambda s: current_ts < s['redeemableUntil']
        )

        return claimable, locked

    def _fetch_non_claimed_snapshots(
        self, snapshot_type: str, contract_name: str
    ) -> List[PerpSnapshot]:
        """
        Fetch snapshots and claims for address.
        """
        snapshots = PerpOffChainStorage.get_epoch_snapshots(snapshot_type)
        rewards_contract = self.w3.eth.contract(
            perp_contract_address(contract_name), abi=rewards_abi
        )

        start, end = snapshots[0]['epoch'], snapshots[-1]['epoch']
        claims = easy_call(
            rewards_contract,
            'claimStatus',
            *[self.address, start, end],
        )

        return [snapshot for snapshot, claimed in zip(snapshots, claims) if not claimed]

    def _get_total_reward(
        self,
        snapshots: List[PerpSnapshot],
        snapshot_filter: Optional[Callable] = None,
    ) -> Decimal:
        """
        Get perp total staking reward.
        """
        rewards = (
            self._get_reward(s)
            for s in snapshots
            if snapshot_filter is None or snapshot_filter(s)
        )
        return sum(rewards) or Decimal(0)

    def _get_reward(self, snapshot: PerpSnapshot) -> Decimal:
        """
        Get single epoch's reward.
        """
        rewards = PerpOffChainStorage.get_rewards(snapshot['epoch'], snapshot['hash'])
        return safe_opt_decimal(
            rewards[self.address]['totalRewardPerp']
            if self.address in rewards
            else None
        )


class PerpetualApi(BlockchainApi, IBalance):
    coin = COIN_PERP
    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM, base_url=None, rate_limit=0.2
    )

    def __init__(self, api_url: str) -> None:
        super().__init__()
        self.w3 = get_eth_client(api_url)

    def get_balance(self, address: str) -> List[BalanceItem]:
        return PerpProtocol(address).fetch_balances()
