# NFT API Test Suite

This directory contains comprehensive test suites for various NFT (Non-Fungible Token) marketplace APIs integrated into the blockapi v2 system. The tests verify the correct functioning of data fetching, parsing, and error handling for multiple NFT platforms across different blockchains.

## Overview

The NFT test suite ensures reliable integration with major NFT marketplaces including MagicEden, OpenSea, SimpleHash, and UniSat. Each test module focuses on a specific marketplace API and validates critical functionality such as:

- Fetching NFT collections, individual tokens, and wallet holdings
- Parsing marketplace-specific data formats into standardized models
- Handling offers, listings, and collection statistics
- Managing API rate limits and retry conditions
- Processing different blockchain standards (ERC721, Ordinals, Runes)

## File Structure

### `__init__.py`
Empty initialization file marking this directory as a Python package.

### `test_magic_eden.py`
Test suite for the MagicEden Solana API integration.

**Key Features:**
- Tests NFT fetching for Solana wallets
- Validates collection statistics parsing
- Tests offer and listing data retrieval
- Handles MagicEden-specific retry conditions for service unavailability
- Uses fixture data from `data/magiceden/` directory

**Test Coverage:**
- `test_parse_nfts`: Validates NFT token parsing from wallet responses
- `test_parse_collection`: Tests collection metadata and statistics
- `test_parse_offers`: Verifies NFT offer (bid) data parsing
- `test_parse_listings`: Tests NFT listing data parsing
- `test_retry_condition`: Ensures proper retry logic for API failures

### `test_opensea.py`
Comprehensive test suite for OpenSea API integration supporting multiple EVM blockchains.

**Key Features:**
- Supports Ethereum and other EVM-compatible chains (including BASE)
- Tests pagination with cursor-based navigation
- Validates locked listing filtering
- Handles API authentication and error responses
- Uses fixture data from `data/opensea/` directory

**Test Coverage:**
- `test_fetch_ntfs`: Tests NFT fetching with pagination
- `test_parse_nfts`: Validates ERC721 NFT parsing
- `test_fetch_offers`: Tests collection offer fetching
- `test_parse_listings`: Validates listing data including locked listings
- `test_parse_collection`: Tests collection statistics across multiple time periods
- `test_supported_blockchains`: Verifies blockchain support

### `test_simple_hash.py`
Test suite for SimpleHash API covering Bitcoin and Solana blockchains.

**Key Features:**
- Tests Bitcoin Ordinals and Runes support
- Handles fungible NFT tokens (Runes)
- Tests listed NFTs with marketplace data
- Validates collection volume and floor price data
- Uses fixture data from `data/simplehash/` directory

**Test Coverage:**
- `test_parse_nfts`: Tests Ordinals NFT parsing with market URLs
- `test_parse_listed_nfts`: Validates Solana NFTs with active listings
- `test_parse_fungible_nfts`: Tests Bitcoin Runes token parsing
- `test_parse_collection`: Validates collection data with floor prices and volumes
- `test_inscriptions_collection`: Special handling for inscription collections
- `test_parse_offers` & `test_parse_listings`: Full offer/listing lifecycle testing

### `test_unisat.py`
Test suite specifically for UniSat API (Bitcoin NFT marketplace).

**Key Features:**
- Focuses on Bitcoin NFT types (Ordinals collections)
- Tests icon URL handling (both relative codes and full URLs)
- Validates offer and listing parsing with BTC amounts
- Uses fixture data from `data/unisat/` directory

**Test Coverage:**
- `test_fetch_collection_icon_code`: Tests automatic CDN URL prefixing for icon codes
- `test_fetch_collection_icon_full_url`: Validates handling of complete icon URLs
- `test_fetch_listings`: Tests listing data with proper BTC decimal conversion
- `test_fetch_offers`: Validates offer filtering by event status

## Integration Points

### Dependencies
- **pytest**: Test framework with custom fixtures
- **requests_mock**: HTTP request mocking for API responses
- **FakeSleepProvider**: Custom sleep provider for rate limit testing
- **blockapi.v2.models**: Standardized NFT data models
- **blockapi.v2.coins**: Cryptocurrency definitions (SOL, ETH, BTC, WETH)

### Data Models Used
- `NftToken`: Individual NFT representation
- `NftCollection`: Collection metadata and statistics
- `NftOffer`: Buy offers and sell listings
- `AssetType`: Token availability status
- `Blockchain`: Chain identifiers
- `NftOfferDirection`: Offer vs Listing classification

### Test Data Location
All test fixtures read JSON response data from:
- `data/magiceden/`: MagicEden API responses
- `data/opensea/`: OpenSea API responses  
- `data/simplehash/`: SimpleHash API responses
- `data/unisat/`: UniSat API responses

## Testing Patterns

1. **Fixture-based Testing**: Each test uses pytest fixtures for API clients and response data
2. **Request Mocking**: All HTTP requests are mocked with pre-recorded responses
3. **Comprehensive Parsing**: Tests validate complete data transformation from raw API responses to domain models
4. **Error Handling**: Tests verify proper error propagation and retry logic
5. **Pagination Support**: Tests validate cursor-based pagination where applicable

## Important Notes

- All monetary values are converted to `Decimal` for precision
- Timestamps are parsed with timezone awareness (UTC)
- NFT identifiers follow platform-specific formats
- Tests ensure backward compatibility with API changes
- Rate limiting is simulated through FakeSleepProvider