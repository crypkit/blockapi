from datetime import datetime
from decimal import Decimal

import pytest

from blockapi.api.kyber import KyberAPI

USER_ADDRESS = '0x1375355fEcCB15e0DBedd7dcF3c496E2b1a25f6A'


class TestKyber:
    @staticmethod
    def test_raises_value_error():
        with pytest.raises(ValueError):
            KyberAPI(USER_ADDRESS, network='ropsten_typo')

    @staticmethod
    @pytest.mark.vcr()
    def test_get_staker_epoch_info():
        info = KyberAPI(USER_ADDRESS, network='ropsten').get_staker_epoch_info(182)
        assert list(info.keys()) == [
            'stake_amount',
            'delegated_stake_amount',
            'pending_stake_amount',
            'delegate',
        ]
        assert [type(val) for val in info.values()] == [Decimal, Decimal, Decimal, str]

    @staticmethod
    @pytest.mark.vcr()
    def test_get_actions():
        actions = KyberAPI(USER_ADDRESS, network='ropsten').get_user_actions()
        assert list(actions[0].keys()) == [
            'epoch',
            'type',
            'tx_hash',
            'meta',
            'action_date',
        ]
        assert [type(val) for val in actions[0].values()] == [
            Decimal,
            str,
            str,
            dict,
            datetime,
        ]

    @staticmethod
    @pytest.mark.vcr()
    def test_get_rewards():
        rewards = KyberAPI(USER_ADDRESS, network='ropsten').get_staker_rewards()
        assert list(rewards[0].keys()) == [
            'epoch',
            'amount',
            'claimed',
            'tx_hash',
            'total_stake',
            'total_reward',
            'total_voted',
        ]
        assert [type(val) for val in rewards[0].values()] == [
            Decimal,
            Decimal,
            bool,
            str,
            Decimal,
            Decimal,
            Decimal,
        ]

    @staticmethod
    @pytest.mark.vcr()
    def test_get_staker_votes():
        votes = KyberAPI(USER_ADDRESS, network='ropsten').get_staker_votes()
        assert list(votes[0].keys()) == [
            'staker',
            'epoch',
            'campaign_id',
            'option',
            'power',
        ]
        assert [type(val) for val in votes[0].values()] == [
            str,
            Decimal,
            Decimal,
            Decimal,
            str,
        ]
