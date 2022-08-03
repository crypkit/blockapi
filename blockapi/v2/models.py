from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Union

import attr

from blockapi.utils.datetime import parse_dt
from blockapi.utils.num import raw_to_decimals, to_decimal, to_int

UNKNOWN = 'unknown'


class Blockchain(str, Enum):
    ARBITRUM = 'arbitrum'
    ASTAR = 'astar'
    AURORA = 'aurora'
    AVALANCHE = 'avalanche'
    AXIE = 'axie'
    BINANCE_SMART_CHAIN = 'binance-smart-chain'
    BITCOIN = 'bitcoin'
    BIT_TORRENT = 'bit-torrent'
    BOBA = 'boba'
    CELO = 'celo'
    CRONOS = 'cronos'
    DEFI_KINGDOMS = 'defi-kingdoms'
    ETHEREUM = 'ethereum'
    EVM_COSMOS = 'evm-cosmos'
    FANTOM = 'fantom'
    FUSE = 'fuse'
    GNOSIS = 'xdai'
    HARMONY = 'harmony'
    HECO = 'heco'
    IOTEX = 'iotex'
    KLAYTN = 'klaytn'
    KU_COIN = 'ku-coin'
    METIS = 'metis'
    MOONBEAM = 'moonbeam'
    MOONBEAM_MOONRIVER = 'moonbeam-moonriver'
    MOONRIVER = 'moonriver'
    OEC = 'okt'
    OPTIMISM = 'optimism'
    PALM = 'palm'
    POLYGON = 'polygon'
    RSK = 'rsk'
    SHIDEN = 'shiden'
    SMART_BITCOIN_CASH = 'smart-bitcoin-cash'
    SOLANA = 'solana'
    SONGBIRD = 'songbird'
    TERRA = 'terra'
    WANCHAIN = 'wanchain'


class AssetType(str, Enum):
    AVAILABLE = 'available'
    CLAIMABLE = 'claimable'
    COLLATERAL = 'collateral'
    COMMON = 'common'
    DEBT = 'debt'
    DEPOSITED = 'deposited'
    FARMING = 'farming'
    LENDING = 'lending'
    LENDING_BORROW = 'lending_borrow'
    LENDING_REWARD = 'lending_reward'
    LIQUIDITY_POOL = 'liquidity_pool'
    LOCKED = 'locked'
    REWARDS = 'rewards'
    STAKED = 'staked'
    UNREALIZED_AVAILABLE = 'unrealized_available'
    VESTING = 'vesting'
    YIELD = 'yield'

    # DEPRECATED
    ASSET = 'asset'


DEBANK_BLOCKCHAIN = {
    'arb': Blockchain.ARBITRUM,
    'avax': Blockchain.AVALANCHE,
    'bsc': Blockchain.BINANCE_SMART_CHAIN,
    'btt': Blockchain.BIT_TORRENT,
    'cro': Blockchain.CRONOS,
    'dfk': Blockchain.DEFI_KINGDOMS,
    'eth': Blockchain.ETHEREUM,
    'evmos': Blockchain.EVM_COSMOS,
    'ftm': Blockchain.FANTOM,
    'hmy': Blockchain.HARMONY,
    'iotx': Blockchain.IOTEX,
    'kcc': Blockchain.KU_COIN,
    'klay': Blockchain.KLAYTN,
    'matic': Blockchain.POLYGON,
    'movr': Blockchain.MOONRIVER,
    'mobm': Blockchain.MOONBEAM,
    'op': Blockchain.OPTIMISM,
    'sbch': Blockchain.SMART_BITCOIN_CASH,
    'sdn': Blockchain.SHIDEN,
    'sgb': Blockchain.SONGBIRD,
    'wan': Blockchain.WANCHAIN,
}

DEBANK_ASSET_TYPES = {
    'vested': AssetType.VESTING,
    'liquidity pool': AssetType.LIQUIDITY_POOL,
}


@attr.s(auto_attribs=True, slots=True)
class ApiOptions:
    blockchain: Blockchain
    base_url: str
    rate_limit: float = 0.0
    testnet: bool = False

    start_offset: Optional[int] = attr.ib(default=None)
    max_items_per_page: Optional[int] = attr.ib(default=None)
    page_offset_step: Optional[int] = attr.ib(default=None)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class CoinInfo:
    tags: List[str] = attr.ib(default=None)
    total_supply: Optional[Decimal] = attr.ib(default=None)
    logo_url: Optional[str] = attr.ib(default=None)
    coingecko_id: Optional[str] = attr.ib(default=None)
    website: Optional[str] = attr.ib(default=None)

    @classmethod
    def from_api(
        cls,
        tags: Optional[List[str]] = None,
        total_supply: Optional[Union[int, float, str]] = None,
        logo_url: Optional[str] = None,
        coingecko_id: Optional[str] = None,
        website: Optional[str] = None,
    ) -> 'CoinInfo':
        return cls(
            tags=tags,
            total_supply=(
                to_decimal(total_supply) if total_supply is not None else None
            ),
            logo_url=logo_url,
            coingecko_id=coingecko_id,
            website=website,
        )


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Coin:
    symbol: str
    name: str
    decimals: int
    blockchain: Blockchain
    address: Optional[str] = attr.ib(default=None)
    standards: Optional[List[str]] = attr.ib(default=None)
    protocol_id: Optional[str] = attr.ib(default=None)
    info: Optional[CoinInfo] = attr.ib(default=None)

    @classmethod
    def from_api(
        cls,
        blockchain: Blockchain,
        decimals: Union[int, str],
        symbol: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        standards: Optional[List[str]] = None,
        protocol_id: Optional[str] = None,
        info: Optional[CoinInfo] = None,
    ) -> 'Coin':
        return cls(
            symbol=symbol if symbol is not None else UNKNOWN,
            name=name if name is not None else UNKNOWN,
            decimals=to_int(decimals) if decimals is not None else 0,
            blockchain=blockchain,
            address=address,
            standards=standards,
            protocol_id=protocol_id,
            info=info,
        )


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Protocol:
    protocol_id: str
    chain: str
    name: str
    user_deposit: Decimal
    site_url: Optional[str] = attr.ib(default=None)
    logo_url: Optional[str] = attr.ib(default=None)
    has_supported_portfolio: bool = attr.ib(default=False)

    @classmethod
    def from_api(
        cls,
        *,
        protocol_id: str,
        chain: str,
        name: str,
        user_deposit: Union[str, float, int],
        site_url: Optional[str] = None,
        logo_url: Optional[str] = None,
        has_supported_portfolio: Optional[bool] = False,
    ) -> 'Protocol':
        return cls(
            protocol_id=protocol_id,
            chain=chain,
            name=name,
            user_deposit=to_decimal(user_deposit),
            site_url=site_url,
            logo_url=logo_url,
            has_supported_portfolio=has_supported_portfolio,
        )


@attr.s(auto_attribs=True, slots=True, frozen=True)
class BalanceItem:
    balance: Decimal
    balance_raw: Decimal
    raw: Dict
    coin: Coin
    asset_type: AssetType = AssetType.AVAILABLE
    last_updated: Optional[datetime] = attr.ib(default=None)
    protocol: Optional[Protocol] = attr.ib(default=None)
    is_wallet: bool = True

    @classmethod
    def from_api(
        cls,
        *,
        balance_raw: Union[int, float, str],
        coin: Coin,
        asset_type: AssetType = AssetType.AVAILABLE,
        raw: Dict,
        last_updated: Optional[Union[int, str]] = None,
        protocol: Optional[Protocol] = None,
        is_wallet: bool = True,
    ) -> 'BalanceItem':
        return cls(
            balance_raw=to_decimal(balance_raw),
            balance=raw_to_decimals(balance_raw, coin.decimals),
            coin=coin,
            asset_type=asset_type,
            raw=raw,
            last_updated=(parse_dt(last_updated) if last_updated is not None else None),
            protocol=protocol,
            is_wallet=is_wallet,
        )

    def __add__(self, other: 'BalanceItem') -> 'BalanceItem':
        """
        Warning: Adding items of different coins leads to wrong results.
        """
        return BalanceItem(
            balance_raw=self.balance_raw + other.balance_raw,
            balance=self.balance + other.balance,
            coin=self.coin,
            asset_type=self.asset_type,
            raw=self._add_raw(other),
            last_updated=self.last_updated,
            protocol=self.protocol,
            is_wallet=self.is_wallet,
        )

    def _add_raw(self, other):
        """
        Used to skip wrapping of "merged" into "merged" key over and over again.
        """
        if self.raw.get("merged") and isinstance(self.raw.get("merged"), list):
            return {"merged": self.raw.get("merged") + [other.raw]}
        else:
            return {"merged": [self.raw, other.raw]}


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Pool:
    pool_id: str
    protocol: Protocol
    items: List[BalanceItem]
    locked_until: Optional[datetime] = attr.ib(default=None)
    health_rate: Optional[Decimal] = attr.ib(default=None)

    @classmethod
    def from_api(
        cls,
        *,
        pool_id: str,
        protocol: Protocol,
        locked_until: Optional[Union[int, str, float]] = None,
        health_rate: Optional[Union[float, str]] = None,
        items: List[BalanceItem],
    ) -> 'Pool':
        return cls(
            pool_id=pool_id,
            protocol=protocol,
            items=items,
            locked_until=(parse_dt(locked_until) if locked_until is not None else None),
            health_rate=to_decimal(health_rate) if health_rate is not None else None,
        )

    def append_items(self, items: List[BalanceItem]) -> 'Pool':
        return Pool(
            pool_id=self.pool_id,
            protocol=self.protocol,
            items=self.items + items,
            locked_until=self.locked_until,
            health_rate=self.health_rate,
        )
