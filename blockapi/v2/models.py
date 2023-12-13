import json
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

import attr

from blockapi.utils.datetime import parse_dt
from blockapi.utils.num import raw_to_decimals, to_decimal, to_int

UNKNOWN = 'unknown'


class Blockchain(str, Enum):
    ACALA = 'acala'
    AKASH = 'akash'
    ALGORAND = 'algorand'
    APTOS = 'aptos'
    ARBITRUM = 'arbitrum'
    ARBITRUM_NOVA = 'arbitrum-nova'
    ARBITRUM_ONE = 'arbitrum-one'
    ARDOR = 'ardor'
    ASTAR = 'astar'
    AURORA = 'aurora'
    AVALANCHE = 'avalanche'
    AXIE = 'axie'
    BASE = 'base'
    BINANCECOIN = 'binancecoin'
    BINANCE_SMART_CHAIN = 'binance-smart-chain'
    BITCICHAIN = 'bitcichain'
    BITCOIN = 'bitcoin'
    BITCOIN_CASH = 'bitcoin-cash'
    BITGERT = 'bitgert'
    BITKUB_CHAIN = 'bitkub-chain'
    BITSHARES = 'bitshares'
    BIT_TORRENT = 'bit-torrent'
    BLOCKNET = 'blocknet'
    BNB_BEACON_CHAIN = 'bnb-beacon-chain'
    BOBA = 'boba'
    BOS = 'bos'
    CALLISTO = 'callisto'
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
    CORE_CHAIN = 'core-chain'
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
    EMPIRE = 'empire'
    ENERGI = 'energi'
    ENQ_ENECUUM = 'enq-enecuum'
    EOS = 'eos'
    ETHEREUM = 'ethereum'
    ETHEREUMPOW = 'ethereumpow'
    ETHEREUM_CLASSIC = 'ethereum-classic'
    EVERSCALE = 'everscale'
    EVMOS = 'evmos'
    EXOSAMA = 'exosama'
    EXPANSE_NETWORK = 'expanse-network'
    FACTOM = 'factom'
    FANTOM = 'fantom'
    FINDORA = 'findora'
    FLARE = 'flare'
    FUNCTION_X = 'function-x'
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
    KUJIRA = 'kujira'
    KUSAMA = 'kusama'
    LINEA = 'linea'
    LITECOIN = 'litecoin'
    LOOT = 'loot'
    LUKSO = 'lukso'
    MANTLE = 'mantle'
    METAVERSE_ETP = 'metaverse-etp'
    METER = 'meter'
    METIS_ANDROMEDA = 'metis-andromeda'
    MILKOMEDA_C1 = 'milkomeda-c1'
    MILKOMEDA_CARDANO = 'milkomeda-cardano'
    MIXIN_NETWORK = 'mixin-network'
    MOONBEAM = 'moonbeam'
    MOONRIVER = 'moonriver'
    NEAR_PROTOCOL = 'near-protocol'
    NEM = 'nem'
    NEO = 'neo'
    NEON_EVM = 'neon-evm'
    NULS = 'nuls'
    NXT = 'nxt'
    OASIS_CHAIN = 'oasis-chain'
    OASIS_EMERALD = 'oasis-emerald'
    OASYS = 'oasys'
    OKEX_CHAIN = 'okex-chain'
    OKT = 'okt'
    OMNI = 'omni'
    ONTOLOGY = 'ontology'
    ONUS_CHAIN = 'onus-chain'
    OPENLEDGER = 'openledger'
    OPEN_NETWORK = 'open-network'
    OPTIMISM = 'optimism'
    OPTIMISTIC_BNB = 'optimistic-bnb'
    OPTIMISTIC_ETHEREUM = 'optimistic-ethereum'
    ORDINALS = 'ordinals'
    OSMOSIS = 'osmosis'
    PALM = 'palm'
    PERSISTENCE = 'persistence'
    PLAT_ON = 'plat-on'
    POLIS_CHAIN = 'polis-chain'
    POLKADOT = 'polkadot'
    POLYGON = 'polygon'
    POLYGON_ZK_EVM = 'polygon-zkevm'
    PROOF_OF_MEMES = 'proof-of-memes'
    PULSE = 'pulse'
    QTUM = 'qtum'
    REGEN = 'regen'
    REI_NETWORK = 'rei-network'
    ROLLUX = 'rollux'
    RONIN = 'ronin'
    ROOTSTOCK = 'rootstock'
    RSK = 'rsk'
    SECRET = 'secret'
    SEED_COIN_NETWORK = 'seed-coin-network'
    SENTINEL = 'sentinel'
    SHIBARIUM = 'shibarium'
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
    SUI = 'sui'
    SUPER_ZERO = 'super-zero'
    SX_NETWORK = 'sx-network'
    SYSCOIN = 'syscoin'
    TBWG_CHAIN = 'tbwg-chain'
    TELOS = 'telos'
    TENET = 'tenet'
    TERRA = 'terra'
    TERRA_2 = 'terra-2'
    TEZOS = 'tezos'
    THAI_CHAIN = 'thai-chain'
    THAI_CHAIN_2_THAI_FI = 'thai-chain-2-thai-fi'
    THETA = 'theta'
    THOR = 'thor'
    THUNDERCORE = 'thundercore'
    TOMBCHAIN = 'tombchain'
    TOMOCHAIN = 'tomochain'
    TRON = 'tron'
    TRUSTLESS_COMPUTER = 'trustless-computer'
    UBIQ = 'ubiq'
    VALORBIT = 'valorbit'
    VECHAIN = 'vechain'
    VELAS = 'velas'
    VITE = 'vite'
    WANCHAIN = 'wanchain'
    WAVES = 'waves'
    WEMIX_NETWORK = 'wemix-network'
    XDAI = 'xdai'
    XDC_NETWORK = 'xdc-network'
    XRP = 'xrp'
    YOCOIN = 'yocoin'
    ZILLIQA = 'zilliqa'
    ZKSYNC_ERA = 'zksync-era'
    ZORA = 'zora'


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
    LENDING_REWARDS = 'lending_reward'
    LIQUIDITY_POOL = 'liquidity_pool'
    LIQUIDITY_POOL_PRINCIPAL = 'liquidity_pool_principal'
    LOCKED = 'locked'
    REWARDS = 'rewards'
    LIQUIDATION_REWARDS = 'liquidation_rewards'
    STAKED = 'staked'
    UNREALIZED_AVAILABLE = 'unrealized_available'
    VESTING = 'vesting'
    PRICED_VESTING = 'priced_vesting'
    YIELD = 'yield'
    PENDING_TRANSACTION = 'pending_transaction'

    # DEPRECATED
    ASSET = 'asset'


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


class CoingeckoId(str, Enum):
    ASTAR = 'astar'
    AURORA = 'aurora-near'
    AVALANCHE = 'avalanche-2'
    BINANCE = 'binancecoin'
    BITCOIN = 'bitcoin'
    BIT_TORRENT = 'bittorrent'
    BOBA = 'boba-network'
    CANTO = 'canto'
    CELO = 'celo'
    COSMOS = 'cosmos'
    CRONOS = 'crypto-com-chain'
    DAI = 'dai'
    DOGECOIN = 'dogecoin'
    ETHEREUM = 'ethereum'
    EVMOS = 'evmos'
    FANTOM = 'fantom'
    FUSE = 'fuse-network-token'
    HARMONY = 'harmony'
    HUOBI = 'huobi-token'
    IOTEX = 'iotex'
    KLAY = 'klaytn'
    KUCOIN = 'kucoin-shares'
    KUSAMA = 'kusama'
    LITECOIN = 'litecoin'
    LUNA = 'terra-luna'
    MATIC = 'matic-network'
    METIS = 'metis-token'
    MOONBEAM = 'moonbeam'
    MOONBEAM_MOONRIVER = 'moonriver'
    OKT = 'oec-token'
    OPTIMISM = 'optimism'
    PERPETUAL = 'perpetual-protocol'
    POLKADOT = 'polkadot'
    PRIME = 'echelon-prime'
    RONIN = 'ronin'
    RSK = 'rootstock'
    SHIDEN = 'shiden'
    SOLANA = 'solana'
    SONGBIRD = 'songbird'
    SYNTHETIX = 'havven'
    TELOS = 'telos'
    USDC = 'usd-coin'
    WANCHAIN = 'wanchain'
    WETH = 'weth'
    XDAI = 'xdai'


class NftOfferDirection(str, Enum):
    OFFER = 'offer'
    LISTING = 'listing'


class OfferItemType(str, Enum):
    NATIVE = 'native'
    ERC20 = 'erc-20'
    ERC721 = 'erc-721'
    ERC1155 = 'erc-1155'
    ERC721_WITH_CRITERIA = 'erc-721-limited'
    ERC1155_WITH_CRITERIA = 'erc-1155-limited'


@attr.s(auto_attribs=True, slots=True)
class ApiOptions:
    blockchain: Blockchain
    base_url: Optional[str]
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
    coingecko_id: Optional[CoingeckoId] = attr.ib(default=None)
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
class CoingeckoMapping:
    symbol: str
    coingecko_id: CoingeckoId
    contracts: set[str]


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
class PoolInfo:
    pool_id: str
    project_id: str
    name: Optional[str] = attr.ib(default=None)
    adapter_id: Optional[str] = attr.ib(default=None)
    controller: Optional[str] = attr.ib(default=None)
    position_index: Optional[str] = attr.ib(default=None)
    tokens: Optional[list[str]] = attr.ib(default=None)

    @classmethod
    def from_api(
        cls,
        *,
        pool_id: str,
        project_id: str,
        name: Optional[str] = None,
        adapter_id: Optional[str] = None,
        controller: Optional[str] = None,
        position_index: Optional[str] = None,
        tokens: Optional[list[str]] = None,
    ) -> 'PoolInfo':
        return cls(
            pool_id=pool_id,
            project_id=project_id,
            name=name,
            adapter_id=adapter_id,
            controller=controller,
            position_index=position_index,
            tokens=tokens,
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
    pool_info: Optional[PoolInfo] = attr.ib(default=None)

    @classmethod
    def from_api(
        cls,
        *,
        balance_raw: Union[int, float, str, Decimal],
        coin: Coin,
        asset_type: AssetType = AssetType.AVAILABLE,
        raw: Dict,
        last_updated: Optional[Union[int, str]] = None,
        protocol: Optional[Protocol] = None,
        is_wallet: bool = True,
        pool_info: Optional[PoolInfo] = None,
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
            pool_info=pool_info,
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
class NftToken:
    ident: str
    collection: str
    contract: str
    standard: str
    name: str
    description: Optional[str]
    amount: Optional[int]
    image_url: str
    metadata_url: Optional[str]
    metadata: Optional[dict]
    updated_time: Optional[datetime]
    is_disabled: bool
    is_nsfw: bool
    asset_type: AssetType
    blockchain: Blockchain

    @classmethod
    def from_api(
        cls,
        *,
        ident: str,
        collection: str,
        contract: str,
        standard: Literal['erc721', 'erc1155'],
        name: str,
        description: str,
        amount: int,
        image_url: str,
        metadata_url: str,
        updated_time: Optional[Union[str, datetime]],
        is_disabled: bool,
        is_nsfw: bool,
        blockchain: Blockchain,
        asset_type: AssetType = AssetType.AVAILABLE,
    ) -> 'NftToken':
        return cls(
            ident=ident,
            collection=collection,
            contract=contract,
            standard=standard,
            name=name,
            description=description,
            amount=int(amount) if amount else 1,
            image_url=image_url,
            metadata_url=metadata_url,
            metadata=None,
            updated_time=parse_dt(updated_time)
            if updated_time and updated_time.strip()
            else None,
            is_disabled=is_disabled,
            is_nsfw=is_nsfw,
            blockchain=blockchain,
            asset_type=asset_type,
        )


@attr.s(auto_attribs=True, slots=True, frozen=True)
class NftOffer:
    offer_key: str
    direction: NftOfferDirection
    collection: str
    contract: str
    blockchain: Blockchain
    offerer: str
    start_time: datetime
    end_time: datetime

    offer_coin: Optional[Coin]
    offer_contract: Optional[str]
    offer_ident: Optional[str]
    offer_amount: Decimal

    pay_coin: Optional[Coin]
    pay_contract: Optional[str]
    pay_ident: Optional[str]
    pay_amount: Decimal

    @classmethod
    def from_api(
        cls,
        *,
        offer_key: str,
        direction: NftOfferDirection,
        collection: str,
        contract: str,
        blockchain: Blockchain,
        offerer: str,
        start_time: str,
        end_time: str,
        offer_coin: Optional[Coin],
        offer_contract: Optional[str],
        offer_ident: Optional[str],
        offer_amount: str,
        pay_coin: Optional[Coin],
        pay_contract: Optional[str],
        pay_ident: Optional[str],
        pay_amount: str,
    ) -> 'NftOffer':
        return cls(
            offer_key=offer_key,
            direction=direction,
            collection=collection,
            contract=contract,
            blockchain=blockchain,
            offerer=offerer,
            start_time=parse_dt(int(start_time)) if start_time else None,
            end_time=parse_dt(int(end_time)) if end_time else None,
            offer_coin=offer_coin,
            offer_contract=offer_contract.lower() if offer_contract else None,
            offer_ident=offer_ident,
            offer_amount=raw_to_decimals(offer_amount, offer_coin.decimals)
            if offer_coin
            else to_decimal(offer_amount),
            pay_coin=pay_coin,
            pay_contract=pay_contract.lower() if pay_contract else None,
            pay_ident=pay_ident,
            pay_amount=raw_to_decimals(pay_amount, pay_coin.decimals)
            if pay_coin
            else to_decimal(pay_amount),
        )


@attr.s(auto_attribs=True, slots=True, frozen=True)
class NftCollectionIntervalStats:
    volume: Decimal
    volume_diff: Decimal
    volume_percent_change: Decimal
    sales_count: int
    sales_diff: int
    average_price: Decimal

    @classmethod
    def from_api(
        cls,
        *,
        volume: str,
        volume_diff: str,
        volume_percent_change: str,
        sales_count: str,
        sales_diff: str,
        average_price: str,
    ) -> 'NftCollectionIntervalStats':
        return cls(
            volume=Decimal(volume),
            volume_diff=Decimal(volume_diff),
            volume_percent_change=Decimal(volume_percent_change),
            sales_count=int(sales_count) if sales_count else 0,
            sales_diff=int(Decimal(sales_diff)) if sales_diff else 0,
            average_price=Decimal(average_price),
        )


@attr.s(auto_attribs=True, slots=True, frozen=True)
class NftCollectionTotalStats:
    volume: Decimal
    sales_count: int
    owners_count: int
    market_cap: Decimal
    floor_price: Decimal
    coin: Coin
    average_price: Decimal

    @classmethod
    def from_api(
        cls,
        *,
        volume: str,
        sales_count: str,
        owners_count: str,
        market_cap: str,
        floor_price: str,
        average_price: str,
        coin: Coin,
    ) -> 'NftCollectionTotalStats':
        return cls(
            volume=Decimal(volume),
            sales_count=int(sales_count) if sales_count else 0,
            owners_count=int(owners_count) if owners_count else 0,
            market_cap=Decimal(market_cap),
            floor_price=Decimal(floor_price),
            average_price=Decimal(average_price),
            coin=coin,
        )


@attr.s(auto_attribs=True, slots=True, frozen=True)
class ContractInfo:
    blockchain: Blockchain
    address: str

    @classmethod
    def from_api(cls, *, blockchain: Blockchain, address: str):
        return cls(blockchain=blockchain, address=address)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class NftCollection:
    ident: str
    name: str
    contracts: list[ContractInfo]
    image: Optional[str]
    is_disabled: bool
    is_nsfw: bool
    blockchain: Blockchain
    total_stats: NftCollectionTotalStats
    day_stats: NftCollectionIntervalStats
    week_stats: NftCollectionIntervalStats
    month_stats: NftCollectionIntervalStats

    @classmethod
    def from_api(
        cls,
        *,
        ident: str,
        name: str,
        contracts: list[ContractInfo],
        image: Optional[str],
        is_disabled: bool,
        is_nsfw: bool,
        blockchain: Blockchain,
        total_stats: NftCollectionTotalStats,
        day_stats: Optional[NftCollectionIntervalStats],
        week_stats: Optional[NftCollectionIntervalStats],
        month_stats: Optional[NftCollectionIntervalStats],
    ) -> 'NftCollection':
        return cls(
            ident=ident,
            name=name,
            contracts=contracts,
            image=image,
            is_disabled=is_disabled,
            is_nsfw=is_nsfw,
            blockchain=blockchain,
            total_stats=total_stats,
            day_stats=day_stats,
            week_stats=week_stats,
            month_stats=month_stats,
        )


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
    pool_info: PoolInfo
    protocol: Protocol
    items: List[BalanceItem]
    locked_until: Optional[datetime] = attr.ib(default=None)
    health_rate: Optional[Decimal] = attr.ib(default=None)

    @classmethod
    def from_api(
        cls,
        *,
        pool_info: PoolInfo,
        protocol: Protocol,
        locked_until: Optional[Union[int, str, float]] = None,
        health_rate: Optional[Union[float, str]] = None,
        items: List[BalanceItem],
    ) -> 'Pool':
        return cls(
            pool_info=pool_info,
            protocol=protocol,
            items=items,
            locked_until=(parse_dt(locked_until) if locked_until is not None else None),
            health_rate=to_decimal(health_rate) if health_rate is not None else None,
        )

    def append_items(self, items: List[BalanceItem]) -> None:
        self.items.extend(items)


@attr.s(auto_attribs=True, slots=True)
class FetchResult:
    status_code: Optional[int] = None
    headers: Optional[dict] = None
    data: Optional[Union[dict, list]] = None
    errors: Optional[list[Union[str, dict]]] = None
    extra: Optional[dict] = None
    cursor: Optional[str] = None
    time: Optional[datetime] = None

    def json(self):
        d = attr.asdict(self)
        return json.dumps({k: v for k, v in d.items() if v}, default=str)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class ParseResult:
    data: Optional[
        list[Union[BalanceItem, Pool, NftToken, NftCollection, NftOffer]]
    ] = None
    warnings: Optional[list[Union[str, dict]]] = None
    errors: Optional[list[Union[str, dict]]] = None
    cursor: Optional[str] = None
    time: Optional[datetime] = None
