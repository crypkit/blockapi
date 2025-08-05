# Blockapi v2 API Directory

## Overview

This directory contains the blockchain API implementations for the blockapi v2 library. It provides unified interfaces for interacting with various blockchain networks, DeFi protocols, NFT marketplaces, and data aggregators. The implementations follow a consistent pattern of inheriting from base classes and implementing standardized interfaces for balance fetching, transaction querying, and specialized blockchain operations.

## Architecture

The API implementations follow these key patterns:
- **Inheritance**: All APIs extend from `BlockchainApi` base class and implement specific interfaces (`IBalance`, `ITransactions`, etc.)
- **Standardization**: Unified data models (`BalanceItem`, `TransactionItem`, `NftToken`, etc.) ensure consistent data format across all blockchains
- **Rate Limiting**: Built-in rate limiting to respect API provider limits
- **Error Handling**: Consistent error handling with custom exceptions for invalid addresses and API errors
- **Modularity**: Subdirectories group related implementations (NFT providers, DeFi protocols, multi-chain aggregators)

## Files and Components

### Core Module Files

- **`__init__.py`**: Main module exports file that exposes all API implementations for easy importing. Includes APIs for Bitcoin, Ethereum, Solana, Cosmos ecosystem, and various aggregators.

- **`web3_utils.py`**: Utility functions for Web3/Ethereum interactions
  - `easy_call()`: Simplified smart contract function calling with error handling
  - `get_eth_client()`: Web3 client initialization
  - `map_struct()`: Maps raw contract results to structured dictionaries
  - Address checksum utilities and decorators

### Native Blockchain APIs

- **`blockchainos.py`**: BOS (Blockchain Operating System) API implementation
  - Fetches BOS token balances and transaction history
  - Parses operations within transactions
  - Uses REST API at `https://mainnet.blockchainos.org`

- **`blockchair.py`**: Multi-blockchain explorer API (Bitcoin, Dogecoin, Litecoin)
  - Implements `BlockchairApi` base class with specialized implementations
  - Supports both regular addresses and extended public keys (xpub)
  - Dashboard API for comprehensive account data
  - Transaction fetching with UTXO model support

- **`cosmos.py`**: Cosmos ecosystem API with support for multiple chains
  - Base class `CosmosApiBase` with implementations for ATOM, OSMOSIS, DYDX, CELESTIA
  - IBC token mapping and native token resolution
  - Staking, unbonding, and rewards balance tracking
  - Dynamic token data loading from GitHub repositories

- **`ethplorer.py`**: Ethereum token balance API
  - ERC20 token discovery and balance fetching
  - Native ETH balance support
  - Token metadata including logos, tags, and Coingecko IDs

- **`optimistic_etherscan.py`**: Optimism L2 Etherscan API
  - Simple ETH balance fetching for Optimism network
  - Etherscan-compatible API interface

- **`solana.py`**: Solana blockchain API with two implementations
  - `SolanaApi`: Direct RPC implementation with SPL token support
    - Metaplex metadata fetching for unknown tokens
    - Staked SOL tracking including rent reserves
    - Token list integration from multiple sources (Jupiter, Solana official)
  - `SolscanApi`: Solscan explorer API for staking data

- **`subscan.py`**: Polkadot/Kusama ecosystem API
  - Abstract `SubscanApi` with implementations for DOT and KSM
  - Complex balance types: available, staked, vesting, reserved
  - Staking rewards and slashes tracking
  - Search API with comprehensive account data

- **`sui.py`**: Sui blockchain API via Blockberry
  - Multi-token balance fetching
  - Coin type formatting and metadata

- **`terra.py`**: Terra blockchain with multiple data sources
  - `TerraApi`: Combines FCD and Mantle APIs
  - `TerraFcdApi`: Native and IBC token balances, staking data
  - `TerraMantleApi`: CW20 token balances via GraphQL
  - Dynamic token list loading from Terra assets

- **`trezor.py`**: Trezor Blockbook API for Bitcoin and Litecoin
  - UTXO-based balance and transaction fetching
  - Support for both addresses and xpubs
  - Transaction details with input/output analysis

### Multi-Chain Aggregators

- **`debank.py`**: DeBank multi-chain DeFi aggregator
  - Comprehensive DeFi protocol integration
  - Portfolio tracking with pools, farming, lending positions
  - Protocol metadata caching system
  - Complex asset type mapping (staking, vesting, debt, etc.)
  - Supports 40+ blockchain networks

- **`debank_maps.py`**: DeBank configuration and mappings
  - Asset type conversions between DeBank and internal models
  - Native coin mappings by blockchain and Coingecko ID
  - Coingecko ID resolution for multi-chain tokens

### Subdirectories

- **`covalenth/`**: Covalenth (formerly Covalent) unified blockchain data API
  - See [covalenth/STRUCTURE.md] for detailed information about multi-chain token balance aggregation

- **`nft/`**: NFT marketplace and aggregator integrations
  - See [nft/STRUCTURE.md] for detailed information about NFT APIs (OpenSea, Magic Eden, SimpleHash, Unisat)

- **`perpetual/`**: Perpetual Protocol DeFi integration
  - See [perpetual/STRUCTURE.md] for detailed information about PERP staking and vesting rewards

- **`synthetix/`**: Synthetix synthetic assets protocol
  - See [synthetix/STRUCTURE.md] for detailed information about SNX staking, debt, and rewards

## Key Integration Patterns

### Balance Fetching
All balance-fetching APIs implement a two-step process:
1. `fetch_balances()`: Retrieves raw data from the blockchain/API
2. `parse_balances()`: Converts raw data to standardized `BalanceItem` objects

### Rate Limiting
Each API defines rate limits in `ApiOptions`:
- Default limits range from 0.05 to 20 requests per second
- Automatic throttling prevents API bans
- Some APIs support API keys for higher limits

### Error Handling
- `InvalidAddressException`: Raised for malformed addresses
- `ApiException`: General API errors with descriptive messages
- Response validation with fallback handling

### Token Resolution
Multiple strategies for token identification:
- On-chain metadata fetching (Solana Metaplex)
- External token lists (Terra, Solana)
- Contract address mapping (Ethereum tokens)
- IBC denom traces (Cosmos)

## Common Dependencies

- `web3`: Ethereum and EVM-compatible chain interactions
- `requests`: HTTP client for REST APIs
- `pydantic`: Data validation for complex response structures
- `eth_utils`: Ethereum address utilities
- `solders`: Solana-specific utilities
- Custom utilities from `blockapi.utils` and `blockapi.v2.base`

## Usage Examples

```python
# Native blockchain balance fetching
from blockapi.v2.api import SolanaApi
api = SolanaApi()
balances = api.get_balance("11111111111111111111111111111111")

# DeFi portfolio aggregation
from blockapi.v2.api import DebankApi
api = DebankApi(api_key="...", is_all=True)
pools = api.get_portfolio("0x...")

# NFT collection data
from blockapi.v2.api.nft import OpenSeaApi
api = OpenSeaApi(api_key="...")
nfts = api.fetch_nfts("0x...")
```

## Important Notes

1. **API Keys**: Many providers require API keys for production use
2. **Rate Limits**: Respect provider limits to avoid bans
3. **Address Formats**: Each blockchain has specific address format requirements
4. **Token Standards**: Different chains use different token standards (ERC20, SPL, CW20, etc.)
5. **Balance Types**: Distinguish between available, staked, vesting, and locked balances