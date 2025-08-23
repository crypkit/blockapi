# Blockapi v2 Directory Structure

## Overview

The v2 directory contains the next-generation blockchain API library for Crypkit, providing a unified interface for interacting with various blockchains, DeFi protocols, and NFT marketplaces. This version introduces a more modular architecture with standardized data models, improved error handling, and support for over 50 blockchain networks.

## Architecture

The v2 library follows several key architectural patterns:

1. **Interface-Based Design**: Abstract interfaces (`IBalance`, `ITransactions`, `IPortfolio`, `INftProvider`) define standard contracts that implementations must follow
2. **Standardized Models**: Unified data models ensure consistent data format across all blockchain integrations
3. **Inheritance Hierarchy**: Base classes (`BlockchainApi`, `CustomizableBlockchainApi`) provide common functionality
4. **Rate Limiting**: Built-in rate limiting with configurable sleep providers
5. **Error Handling**: Consistent exception types and error propagation

## Directory Structure

```
v2/
├── __init__.py                 # Package initialization (empty)
├── base.py                     # Core base classes and interfaces
├── blockchain_mapping.py       # Blockchain identifier mapping utilities
├── coin_mapping.py            # Coin/token mapping configurations
├── coins.py                   # Pre-defined coin/token definitions
├── models.py                  # Data models and enumerations
└── api/                       # API implementations directory
    ├── STRUCTURE.md           # Detailed API documentation
    ├── covalenth/            # Multi-chain token aggregator
    ├── nft/                  # NFT marketplace integrations
    ├── perpetual/            # Perpetual Protocol integration
    └── synthetix/            # Synthetix protocol integration
```

## Core Files

### `base.py`
The foundation of the v2 architecture, containing:

**Key Classes:**
- `ISleepProvider` / `SleepProvider`: Rate limiting through configurable sleep mechanisms
- `CustomizableBlockchainApi`: Abstract base for APIs with customizable endpoints (proxy support, testnets, alternative RPC)
- `BlockchainApi`: Standard blockchain API base class
- `BalanceMixin`: Reusable implementation of balance fetching pattern

**Core Interfaces:**
- `IBalance`: Contract for balance-fetching implementations
- `ITransactions`: Contract for transaction history retrieval
- `IPortfolio`: Contract for DeFi portfolio data
- `INftProvider` / `INftParser`: Contracts for NFT data fetching and parsing
- `IBlockchainFetcher` / `IBlockchainParser`: Generic fetch/parse pattern interfaces

**Exception Types:**
- `ApiException`: General API errors
- `InvalidAddressException`: Malformed blockchain addresses

**Features:**
- HTTP session management with automatic cleanup
- Retry logic for rate limits and connection errors
- Response time tracking from headers
- Configurable JSON parsing arguments
- Built-in error response handling

### `blockchain_mapping.py`
Utilities for mapping blockchain identifiers across different systems:

**Mapping Functions:**
- `get_blockchain_from_debank_chain()`: Maps DeBank chain IDs to internal Blockchain enum
- `get_blockchain_from_coingecko_chain()`: Maps CoinGecko platform IDs
- `get_blockchain_from_chain_id()`: Maps EVM chain IDs (e.g., 1 for Ethereum)
- `get_blockchain_from_rango_chain()`: Maps Rango exchange identifiers
- `get_blockchain_from_wormhole_chain()`: Maps Wormhole bridge identifiers

**Key Mappings:**
- DeBank: 97 blockchain mappings (most comprehensive)
- CoinGecko: 40 platform mappings
- Chain ID: 74 EVM network mappings
- Supports automatic fallback to Blockchain enum values

### `coin_mapping.py`
Token/coin mapping configurations for specific integrations:

**Current Mappings:**
- `OPENSEA_COINS`: Maps OpenSea payment token symbols to Coin objects
- `OPENSEA_CONTRACTS`: Maps contract addresses to specific coins (WETH, ETH)

**Supported OpenSea Tokens:**
- ETH, USDC, PRIME, DAI, MATIC

### `coins.py`
Pre-defined coin/token definitions used throughout the library:

**Native Coins Defined:**
- Ethereum: ETH, WETH
- Solana: SOL
- Terra: LUNA
- Polygon: MATIC
- Avalanche: AVAX
- Various other native tokens for 50+ blockchains

**Coin Properties:**
- Symbol, name, decimals
- Blockchain association
- Contract address (for tokens)
- Metadata: logo URLs, CoinGecko IDs, websites
- Token standards supported

### `models.py`
Comprehensive data models and enumerations:

**Key Enumerations:**
- `Blockchain`: 200+ blockchain identifiers
- `AssetType`: Classification of assets (AVAILABLE, STAKED, REWARDS, DEBT, etc.)
- `CoingeckoId`: 1000+ CoinGecko cryptocurrency IDs
- `ProtocolType`: DeFi protocol classifications
- `Chain`: Simplified chain names for specific integrations

**Core Data Models:**
- `Coin`: Token/coin definition with metadata
- `CoinInfo`: Extended coin metadata (logos, tags, links)
- `BalanceItem`: Standardized balance representation
- `TransactionItem`: Blockchain transaction data
- `Pool`: DeFi pool/position information
- `NftToken`, `NftCollection`, `NftOffer`: NFT-related models
- `FetchResult`, `ParseResult`: API operation results

**Model Features:**
- Automatic decimal conversion
- DateTime parsing utilities
- JSON serialization support
- Optional field handling
- Nested data structure support

## API Subdirectory

The `api/` subdirectory contains all blockchain-specific implementations. See [api/STRUCTURE.md](api/STRUCTURE.md) for detailed information about:
- Native blockchain APIs (Bitcoin, Ethereum, Solana, etc.)
- Multi-chain aggregators (DeBank, Covalenth)
- DeFi protocol integrations (Synthetix, Perpetual)
- NFT marketplace APIs (OpenSea, Magic Eden, etc.)

### Key Subdirectories:
- **`covalenth/`**: See [api/covalenth/STRUCTURE.md](api/covalenth/STRUCTURE.md) for multi-chain token balance aggregation
- **`nft/`**: See [api/nft/STRUCTURE.md](api/nft/STRUCTURE.md) for NFT marketplace integrations
- **`perpetual/`**: See [api/perpetual/STRUCTURE.md](api/perpetual/STRUCTURE.md) for Perpetual Protocol staking/vesting
- **`synthetix/`**: See [api/synthetix/STRUCTURE.md](api/synthetix/STRUCTURE.md) for Synthetix synthetic assets

## Usage Patterns

### Basic Balance Fetching
```python
from blockapi.v2.api import SolanaApi

api = SolanaApi()
balances = api.get_balance("11111111111111111111111111111111")
```

### Custom RPC Endpoint
```python
from blockapi.v2.api import EthereumApi

api = EthereumApi(base_url="https://mainnet.infura.io/v3/YOUR_KEY")
balances = api.get_balance("0x...")
```

### NFT Data Retrieval
```python
from blockapi.v2.api.nft import OpenSeaApi

api = OpenSeaApi(api_key="...", blockchain=Blockchain.ETHEREUM)
result = api.fetch_nfts("0x...")
parsed = api.parse_nfts(result)
```

### DeFi Portfolio
```python
from blockapi.v2.api import DebankApi

api = DebankApi(api_key="...", is_all=True)
portfolio = api.get_portfolio("0x...")
```

## Design Principles

1. **Modularity**: Each blockchain/protocol has its own implementation file
2. **Consistency**: All APIs follow the same patterns and return standardized models
3. **Extensibility**: New blockchains can be added by implementing base interfaces
4. **Error Resilience**: Graceful degradation with detailed error information
5. **Performance**: Built-in caching, session reuse, and rate limit management

## Dependencies

- **Core**: requests, attrs, pydantic
- **Blockchain-Specific**: web3 (Ethereum), solders (Solana)
- **Utilities**: eth_utils, beautifulsoup4, marko
- **Internal**: blockapi.utils for number/datetime utilities

## Important Notes

1. Most APIs require API keys for production use
2. Rate limits vary by provider (configured in ApiOptions)
3. Address formats are blockchain-specific and validated
4. All monetary values use Decimal for precision
5. Timestamps are standardized to UTC datetime objects