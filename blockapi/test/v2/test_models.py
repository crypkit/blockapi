from decimal import Decimal

from blockapi.v2.coins import COIN_ETH
from blockapi.v2.models import BalanceItem, Blockchain, Protocol


def test_create_protocol_from_api():
    protocol = Protocol.from_api(
        protocol_id="0xmons",
        chain=Blockchain.ETHEREUM,
        name="0xmons_name",
        user_deposit=1234.5,
        site_url="https://0xmons.xyz",
        logo_url="https://static.debank.com/image/project/logo_url/0xmons/125fd50693dcfb1a1c4a720fb27f017d.png",
        has_supported_portfolio=True,
    )

    assert protocol.protocol_id == '0xmons'
    assert protocol.chain == Blockchain.ETHEREUM
    assert protocol.name == '0xmons_name'
    assert protocol.site_url == 'https://0xmons.xyz'
    assert (
        protocol.logo_url == 'https://static.debank.com/image/project/logo_url/0xmons/'
        '125fd50693dcfb1a1c4a720fb27f017d.png'
    )
    assert protocol.has_supported_portfolio is True
    assert protocol.user_deposit == Decimal(1234.5)


def test_balance_has_protocol():
    balance = BalanceItem.from_api(balance_raw="3", coin=COIN_ETH, raw={})
    assert balance.protocol is None


def test_balance_protocol_can_be_set():
    protocol = Protocol.from_api(
        protocol_id="x", chain=Blockchain.ETHEREUM, name="X", user_deposit=4
    )
    balance = BalanceItem.from_api(
        balance_raw="3", coin=COIN_ETH, raw={}, protocol=protocol
    )
    assert balance.protocol == protocol
