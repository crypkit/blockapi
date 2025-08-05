# NFT API Module Structure

## Overview
This directory contains NFT (Non-Fungible Token) API implementations for various blockchain marketplaces and aggregators. It provides unified interfaces for fetching NFT data, collections, listings, and offers across multiple platforms including Magic Eden, OpenSea, SimpleHash, and Unisat.

## Architecture
All NFT API implementations follow a consistent pattern:
- Inherit from `BlockchainApi` base class
- Implement `INftProvider` and `INftParser` interfaces
- Use standardized data models from `blockapi.v2.models`
- Handle rate limiting through sleep providers
- Return data in unified `FetchResult` and `ParseResult` formats

## Files

### `__init__.py`
**Purpose**: Package initialization and public API exports
- Exports all NFT API implementations for easy importing
- Provides centralized access to:
  - `MagicEdenSolanaApi`: Solana NFT marketplace
  - `OpenSeaApi`: Multi-chain NFT marketplace (Ethereum-based)
  - `SimpleHashBitcoinApi`: Bitcoin ordinals/inscriptions
  - `SimpleHashEthereumApi`: Ethereum and EVM-compatible chains
  - `SimpleHashSolanaApi`: Solana NFTs via SimpleHash
  - `UnisatApi`: Bitcoin ordinals marketplace

### `magic_eden.py`
**Purpose**: Magic Eden marketplace API integration for Solana NFTs
- **Key Features**:
  - Fetches NFTs by wallet address with pagination
  - Retrieves collection statistics and metadata
  - Handles listings and pool-based offers
  - Implements retry logic for service unavailability
- **API Endpoints**:
  - `wallets/{address}/tokens`: Get NFTs owned by address
  - `collections/{slug}/stats`: Collection statistics
  - `collections/{slug}/listings`: Active listings
  - `mmm/pools`: AMM pool offers
- **Rate Limiting**: ~2 requests per second
- **Special Handling**:
  - Calculates offer prices including fees (seller, LP, taker)
  - Filters duplicate offers by UUID
  - Handles service unavailable errors with 60-second retry

### `opensea.py`
**Purpose**: OpenSea API integration for multi-chain NFT marketplaces
- **Supported Blockchains**:
  - Ethereum, Arbitrum, Avalanche, Base, BSC, Klaytn, Optimism, Polygon, Zora
- **Key Features**:
  - Paginated NFT fetching with cursor support
  - Collection data with floor prices and statistics
  - Offers and listings with Seaport protocol parsing
  - Multi-chain contract resolution
- **API Endpoints**:
  - `chain/{chain}/account/{address}/nfts`: NFTs by owner
  - `offers/collection/{collection}/all`: Collection offers
  - `listings/collection/{collection}/all`: Active listings
  - `collections/{collection}`: Collection metadata
  - `collections/{collection}/stats`: Trading statistics
- **Rate Limiting**: 4 requests per second
- **Special Handling**:
  - Maps OpenSea-specific blockchain names
  - Parses complex Seaport offer structures
  - Handles multiple offer items and considerations
  - Implements retry-after header support

### `simple_hash.py`
**Purpose**: SimpleHash API integration - unified NFT data aggregator
- **Three Specialized Implementations**:
  1. **SimpleHashBitcoinApi**: Bitcoin ordinals and inscriptions
     - Handles both NFTs and fungibles (Runes)
     - Special collection mapping for inscriptions
     - Default collection: "inscriptions"
  2. **SimpleHashSolanaApi**: Solana NFTs
     - Combines NFT and listing data
     - Wallet-specific listings support
  3. **SimpleHashEthereumApi**: Ethereum and EVM chains
     - Supports 12+ EVM-compatible blockchains
- **Key Features**:
  - Unified API across multiple blockchains
  - Rich metadata including floor prices and volumes
  - Bid/offer ordering and filtering
  - Fungible token support (Runes on Bitcoin)
- **API Endpoints**:
  - `nfts/owners`: NFTs by wallet
  - `fungibles/balances`: Fungible tokens
  - `nfts/collections/ids`: Collection details
  - `nfts/bids/collection`: Collection offers
  - `nfts/listings/collection`: Active listings
- **Rate Limiting**: 100 requests per second (free tier)
- **Special Handling**:
  - Multi-cursor pagination for different data types
  - Dynamic coin mapping from payment tokens
  - Marketplace URL prioritization (Magic Eden > OpenSea)

### `unisat.py`
**Purpose**: Unisat API integration for Bitcoin ordinals marketplace
- **Key Features**:
  - Bitcoin inscription/ordinal fetching
  - Collection statistics and metadata
  - Listings and historical offer data
  - BRC-20 and domain name support
- **API Endpoints**:
  - `indexer/address/{address}/inscription-data`: Inscriptions by owner
  - `market/collection/auction/list`: Active listings
  - `market/collection/auction/actions`: Historical events
  - `market/collection/auction/collection_statistic`: Stats
  - `market/collection/auction/collection_summary`: Collection mapping
- **Rate Limiting**: 5 requests per second (free tier)
- **Special Handling**:
  - Builds collection mapping from summary endpoint
  - Handles "uncategorized-ordinals" as default collection
  - Converts icon URLs to full paths
  - Dummy result generation for server errors
  - Timestamp conversion from milliseconds to ISO format

## Common Patterns

### Error Handling
- All APIs return `FetchResult` objects with error arrays
- Parse methods handle missing/malformed data gracefully
- Retry logic for rate limits and service unavailability

### Data Normalization
- Unified `NftToken` model for all NFT data
- Standardized `NftCollection` with statistics
- Consistent `NftOffer` format for listings/offers
- Price conversions to decimal format

### Rate Limiting
- Each API respects platform-specific rate limits
- Sleep providers handle request throttling
- Retry-after headers honored (OpenSea)

### Pagination
- Cursor-based pagination where supported
- Offset/limit pagination fallback
- Maximum offset limits enforced (e.g., 15000 for Magic Eden)

## Integration Points
- Uses coin mappings from `blockapi.v2.coins`
- Leverages base classes from `blockapi.v2.base`
- Returns standardized models from `blockapi.v2.models`
- Integrates with sleep providers for rate limiting

## Usage Example
```python
# Initialize API
api = OpenSeaApi(api_key="...", blockchain=Blockchain.ETHEREUM)

# Fetch NFTs
result = api.fetch_nfts("0x123...")
parsed = api.parse_nfts(result)

# Get collection data
collection_result = api.fetch_collection("cryptopunks")
collection_data = api.parse_collection(collection_result)
```