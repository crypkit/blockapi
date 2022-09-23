from datetime import datetime
from decimal import Decimal
from typing import Dict, List

from blockapi.services import BlockchainAPI


class KyberAPI(BlockchainAPI):
    """
    Kyber Network
    API docs: https://github.com/KyberNetwork/developer-portal/blob/
                                    stakingSection/api-endpoints.md
    Explorer: https://tracker.kyber.network/#/trades
    """

    symbol = 'KNC'
    supported_requests = {
        'get_staker_epoch_info': 'stakers/{address}?epoch={epoch}',
        'get_user_actions': 'stakers/{address}/actions',
        'get_staker_rewards': 'stakers/{address}/rewards',
        'get_staker_votes': 'stakers/{address}/votes',
    }

    def __init__(self, address: str, network: str = 'mainnet'):
        ENDPOINTS = {
            'mainnet': 'https://api.kyber.org/',
            'ropsten': 'https://ropsten-api.kyber.org/',
        }
        if network not in ENDPOINTS.keys():
            raise ValueError(
                f'Network has to be one of {list(ENDPOINTS.keys())}. '
                f'Received \'{network}\' instead.'
            )
        self.base_url = ENDPOINTS[network]

        super(KyberAPI, self).__init__(address)

    def get_staker_epoch_info(self, epoch: int) -> Dict:
        """
        Get staker information for a given epoch

        return: a dict with the following info:
            {
                "stake_amount": Decimal,
                "delegated_stake_amount": Decimal,
                "pending_stake_amount": Decimal,
                "delegate": str, - Ethereum address of the delegate
            }
        """
        result = self.request(
            'get_staker_epoch_info', address=self.address, epoch=epoch
        )
        if not result['success'] or not result['data']:
            return {}
        return self._parse_staker_epoch_info(result['data'])

    @staticmethod
    def _parse_staker_epoch_info(info: Dict) -> Dict:
        return {
            'stake_amount': Decimal(info['stake_amount']),
            'delegated_stake_amount': Decimal(info['delegated_stake_amount']),
            'pending_stake_amount': Decimal(info['pending_stake_amount']),
            'delegate': info['delegate'],
        }

    def get_user_actions(self) -> List[Dict]:
        """
        Get information about actions undertaken by a given address

        return: a list of dicts with the following info:
            {
                'epoch': Decimal, Epoch number
                'type': str, A type of action executed (e.g. Deposit)
                'tx_hash': str, A tx hash of a given action
                'meta': dict, Additional info (amount, campaign_id, option)
                'action_date': datetime, A date and time of the action
            }
        """
        result = self.request('get_user_actions', address=self.address)
        if not result['success'] or not result['data']:
            return []
        return self._parse_user_actions(result['data'])

    @staticmethod
    def _parse_user_actions(raw_actions: List) -> List[Dict]:
        actions = []
        for action in raw_actions:
            actions.append(
                {
                    'epoch': Decimal(action['epoch']),
                    'type': action['type'],
                    'tx_hash': action['tx_hash'],
                    'meta': action['meta'],
                    'action_date': datetime.utcfromtimestamp(action['timestamp']),
                }
            )
        return actions

    def get_staker_rewards(self) -> List[Dict]:
        """
        Get information about staking rewards for a given address

        return: a list of dicts with the following info:
            {
                'epoch': Decimal, Epoch number
                'amount': Decimal, ETH reward claimable / claimed for staker
                            and his pool members
                'claimed': bool, Says, whether reward has been claimed
                'tx_hash': str, Transaction hash of the reward claim
                'total_stake': Decimal, Total KNC stake of the staker and other
                                pool members
                'total_reward': Decimal, Total ETH reward claimable by all
                                stakers for epoch
                'total_voted': Decimal, Total vote amount by all stakers for
                                epoch
            }
        """
        result = self.request('get_staker_rewards', address=self.address)
        if not result['success'] or not result['data']:
            return []
        return self._parse_staker_rewards(result['data'])

    @staticmethod
    def _parse_staker_rewards(raw_rewards: List) -> List[Dict]:
        rewards = []
        for reward in raw_rewards:
            rewards.append(
                {
                    'epoch': Decimal(reward['epoch']),
                    'amount': Decimal(reward['amount']),
                    'claimed': reward['claimed'],
                    'tx_hash': reward['tx_hash'],
                    'total_stake': Decimal(reward['total_stake']),
                    'total_reward': Decimal(reward['total_reward']),
                    'total_voted': Decimal(reward['total_voted']),
                }
            )
        return rewards

    def get_staker_votes(self) -> List[Dict]:
        """
        Get information about actions undertaken by a given address

        return: a list of dicts with the following info:
            {
                'staker': str, Staker's address
                'epoch': Decimal, Epoch number
                'campaign_id': Decimal, Campaign ID number
                'option': Decimal, Voted option by stake
                'power': str, Voting power of staker (delegations accounted
                for)
            }
        """
        result = self.request('get_staker_votes', address=self.address)
        if not result['success'] or not result['data']:
            return []
        return self._parse_staker_votes(result['data'])

    @staticmethod
    def _parse_staker_votes(raw_votes: List) -> List[Dict]:
        votes = []
        for vote in raw_votes:
            votes.append(
                {
                    'staker': vote['staker'],
                    'epoch': Decimal(vote['epoch']),
                    'campaign_id': Decimal(vote['campaign_id']),
                    'option': Decimal(vote['option']),
                    'power': vote['power'],
                }
            )
        return votes

    def get_balance(self):
        return None
