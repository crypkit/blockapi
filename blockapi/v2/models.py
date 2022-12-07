from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Union

import attr

from blockapi.utils.datetime import parse_dt
from blockapi.utils.num import raw_to_decimals, to_decimal, to_int

UNKNOWN = 'unknown'


class Blockchain(str, Enum):
    ACALA = 'acala'
    AKASH = 'akash'
    ALGORAND = 'algorand'
    ARBITRUM = 'arbitrum'
    ARBITRUM_NOVA = 'arbitrum-nova'
    ARBITRUM_ONE = 'arbitrum-one'
    ARDOR = 'ardor'
    ASTAR = 'astar'
    AURORA = 'aurora'
    AVALANCHE = 'avalanche'
    AXIE = 'axie'
    BINANCECOIN = 'binancecoin'
    BINANCE_SMART_CHAIN = 'binance-smart-chain'
    BITCICHAIN = 'bitcichain'
    BITCOIN = 'bitcoin'
    BITCOIN_CASH = 'bitcoin-cash'
    BITGERT = 'bitgert'
    BITSHARES = 'bitshares'
    BIT_TORRENT = 'bit-torrent'
    BLOCKNET = 'blocknet'
    BNB_BEACON_CHAIN = 'bnb-beacon-chain'
    BOBA = 'boba'
    BOS = 'bos'
    CANTO = 'canto'
    CARDANO = 'cardano'
    CELER_NETWORK = 'celer-network'
    CELO = 'celo'
    CHILIZ = 'chiliz'
    CLV_PARACHAIN = 'clv-parachain'
    CMP = 'cmp'
    COINEX_SMART_CHAIN = 'coinex-smart-chain'
    COLOSSUSXT = 'colossusxt'
    CONFLUX = 'conflux'
    COSMOS = 'cosmos'
    COUNTERPARTY = 'counterparty'
    CRONOS = 'cronos'
    CRYPTO_ORG = 'crypto-org'
    CUBE = 'cube'
    DARWINIA_CRAB_NETWORK = 'darwinia-crab-network'
    DASH = 'dash'
    DEFI_KINGDOMS = 'defi-kingdoms'
    DFK_CHAIN = 'dfk-chain'
    DITHEREUM = 'dithereum'
    DOGECHAIN = 'dogechain'
    DXCHAIN = 'dxchain'
    ECHELON = 'echelon'
    ELASTOS = 'elastos'
    ELA_DID_SIDECHAIN = 'ela-did-sidechain'
    ELROND = 'elrond'
    EMERALD_PARATIME = 'emerald-paratime'
    ENERGI = 'energi'
    ENQ_ENECUUM = 'enq-enecuum'
    EOS = 'eos'
    ETHEREUM = 'ethereum'
    ETHEREUMPOW = 'ethereumpow'
    ETHEREUM_CLASSIC = 'ethereum-classic'
    EVERSCALE = 'everscale'
    EVMOS = 'evmos'
    EXPANSE_NETWORK = 'expanse-network'
    FACTOM = 'factom'
    FANTOM = 'fantom'
    FINDORA = 'findora'
    FLARE = 'flare'
    FUSE = 'fuse'
    FUSION_NETWORK = 'fusion-network'
    GENESIS_L1 = 'genesis-l1'
    GNOSIS = 'gnosis'
    GOCHAIN = 'gochain'
    GODWOKEN = 'godwoken'
    HARMONY = 'harmony'
    HECO = 'heco'
    HEDERA_HASHGRAPH = 'hedera-hashgraph'
    HOO_SMART_CHAIN = 'hoo-smart-chain'
    HUOBI_TOKEN = 'huobi-token'
    HYDRA = 'hydra'
    ICON = 'icon'
    IOTEX = 'iotex'
    IRIS = 'iris'
    JUNO = 'juno'
    KARDIACHAIN = 'kardiachain'
    KARURA = 'karura'
    KAVA = 'kava'
    KCC = 'kcc'
    KLAYTN_CYPRESS = 'klaytn-cypress'
    KLAY_TOKEN = 'klay-token'
    KOMODO = 'komodo'
    KUCOIN = 'kucoin'
    KUSAMA = 'kusama'
    LITECOIN = 'litecoin'
    METAVERSE_ETP = 'metaverse-etp'
    METER = 'meter'
    METIS_ANDROMEDA = 'metis-andromeda'
    MILKOMEDA_C1 = 'milkomeda-c1'
    MILKOMEDA_CARDANO = 'milkomeda-cardano'
    MIXIN_NETWORK = 'mixin-network'
    MOONBEAM = 'moonbeam'
    MOONBEAM_MOONRIVER = 'moonbeam-moonriver'
    MOONRIVER = 'moonriver'
    NEAR_PROTOCOL = 'near-protocol'
    NEM = 'nem'
    NEO = 'neo'
    NULS = 'nuls'
    NXT = 'nxt'
    OASIS = 'oasis'
    OKEX_CHAIN = 'okex-chain'
    OKT = 'okt'
    OMNI = 'omni'
    ONTOLOGY = 'ontology'
    OPENLEDGER = 'openledger'
    OPTIMISM = 'optimism'
    OPTIMISTIC_ETHEREUM = 'optimistic-ethereum'
    OSMOSIS = 'osmosis'
    PALM = 'palm'
    PERSISTENCE = 'persistence'
    PLAT_ON = 'plat-on'
    POLIS_CHAIN = 'polis-chain'
    POLKADOT = 'polkadot'
    POLYGON = 'polygon'
    QTUM = 'qtum'
    REGEN = 'regen'
    REI_NETWORK = 'rei-network'
    RONIN = 'ronin'
    ROOTSTOCK = 'rootstock'
    SECRET = 'secret'
    SEED_COIN_NETWORK = 'seed-coin-network'
    SENTINEL = 'sentinel'
    SHIBA_CHAIN = 'shiba-chain'
    SHIDEN_NETWORK = 'shiden-network'
    SIFCHAIN = 'sifchain'
    SKALE = 'skale'
    SMART_BITCOIN_CASH = 'smart-bitcoin-cash'
    SOLANA = 'solana'
    SONGBIRD = 'songbird'
    SONGBIRD_CANARY = 'songbird-canary'
    SORA = 'sora'
    STACKS = 'stacks'
    STELLAR = 'stellar'
    STEP_NETWORK = 'step-network'
    STRATIS = 'stratis'
    SUPER_ZERO = 'super-zero'
    SX_NETWORK = 'sx-network'
    SYSCOIN = 'syscoin'
    TBWG_CHAIN = 'tbwg-chain'
    TELOS = 'telos'
    TERRA = 'terra'
    TEZOS = 'tezos'
    THAI_CHAIN = 'thai-chain'
    THAI_CHAIN_2_THAI_FI = 'thai-chain-2-thai-fi'
    THETA = 'theta'
    THOR = 'thor'
    THUNDERCORE = 'thundercore'
    TOMBCHAIN = 'tombchain'
    TOMOCHAIN = 'tomochain'
    TRON = 'tron'
    UBIQ = 'ubiq'
    VALORBIT = 'valorbit'
    VECHAIN = 'vechain'
    VELAS = 'velas'
    VITE = 'vite'
    WANCHAIN = 'wanchain'
    WAVES = 'waves'
    XDAI = 'xdai'
    XDC_NETWORK = 'xdc-network'
    XRP = 'xrp'
    YOCOIN = 'yocoin'
    ZILLIQA = 'zilliqa'


class AssetType(str, Enum):
    AVAILABLE = 'available'
    CLAIMABLE = 'claimable'
    COLLATERAL = 'collateral'
    COMMON = 'common'
    DEBT = 'debt'
    DEPOSITED = 'deposited'
    FARMING = 'farming'
    INVESTMENT = 'investment'
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


class TokenRole(str, Enum):
    SUPPLY = 'supply'
    REWARD = 'reward'
    BORROW = 'borrow'
    LIQUIDITY_POOL = 'liquidity_pool'


class OperationType(str, Enum):
    UNKNOWN = 'unknown'
    INFLATION = 'inflation'
    TRANSACTION = 'transaction'
    COLLECT_TX_FEE = 'collect-tx-fee'


class OperationDirection(str, Enum):
    OUTGOING = 'outgoing'
    INCOMING = 'incoming'


class TransactionStatus(str, Enum):
    CONFIRMED = 'confirmed'
    PENDING = 'pending'


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
    chain: Blockchain
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
        chain: Blockchain,
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
    token_set: Optional[List[str]] = attr.ib(default=None)
    token_role: Optional[TokenRole] = attr.ib(default=None)
    pool_id: Optional[str] = attr.ib(default=None)

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
        token_set: Optional[List[str]] = None,
        token_role: Optional[TokenRole] = None,
        pool_id: Optional[str] = None,
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
            token_set=token_set,
            token_role=token_role,
            pool_id=pool_id,
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
class OperationItem:
    amount: Decimal
    amount_raw: Decimal
    coin: Coin
    from_address: str
    to_address: str
    hash: str
    type: OperationType
    direction: OperationDirection
    confirmed: Optional[datetime]
    raw: dict

    @classmethod
    def from_api(
        cls,
        *,
        amount_raw: Union[int, float, str],
        coin: Coin,
        from_address: str,
        to_address: str,
        hash: str,
        type: OperationType,
        direction: OperationDirection,
        raw: dict,
        confirmed: Optional[Union[int, str]] = None,
    ) -> 'OperationItem':
        return cls(
            amount_raw=to_decimal(amount_raw),
            amount=raw_to_decimals(amount_raw, coin.decimals),
            coin=coin,
            from_address=from_address,
            to_address=to_address,
            hash=hash,
            type=type,
            direction=direction,
            confirmed=(parse_dt(confirmed) if confirmed is not None else None),
            raw=raw,
        )


@attr.s(auto_attribs=True, slots=True, frozen=True)
class TransactionItem:
    fee: Decimal
    fee_raw: Decimal
    date: datetime
    coin: Coin
    hash: str
    status: TransactionStatus
    operations: List[OperationItem]
    raw: dict

    @classmethod
    def from_api(
        cls,
        *,
        fee_raw: Union[int, float, str],
        coin: Coin,
        date: Union[int, str],
        hash: str,
        status: TransactionStatus = TransactionStatus.CONFIRMED,
        operations: List[OperationItem],
        raw: dict,
    ) -> 'TransactionItem':
        return cls(
            fee_raw=to_decimal(fee_raw or '0'),
            fee=raw_to_decimals(fee_raw or '0', coin.decimals),
            coin=coin,
            date=(parse_dt(date) if date is not None else None),
            hash=hash,
            status=status,
            operations=operations,
            raw=raw,
        )


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Pool:
    pool_id: str
    protocol: Protocol
    items: List[BalanceItem]
    locked_until: Optional[datetime] = attr.ib(default=None)
    health_rate: Optional[Decimal] = attr.ib(default=None)
    token_set: Optional[str] = attr.ib(default=None)
    project_id: Optional[str] = attr.ib(default=None)
    adapter_id: Optional[str] = attr.ib(default=None)

    @classmethod
    def from_api(
        cls,
        *,
        pool_id: str,
        protocol: Protocol,
        locked_until: Optional[Union[int, str, float]] = None,
        health_rate: Optional[Union[float, str]] = None,
        items: List[BalanceItem],
        token_set: Optional[str] = None,
        project_id: Optional[str] = None,
        adapter_id: Optional[str] = None,
    ) -> 'Pool':
        return cls(
            pool_id=pool_id,
            protocol=protocol,
            items=items,
            locked_until=(parse_dt(locked_until) if locked_until is not None else None),
            health_rate=to_decimal(health_rate) if health_rate is not None else None,
            token_set=token_set,
            project_id=project_id,
            adapter_id=adapter_id,
        )

    def append_items(self, items: List[BalanceItem]) -> None:
        self.items.extend(items)
