# Blockapi V2 API Test Suite

## Overview

This directory contains the comprehensive test suite for the blockapi v2 API integrations. It includes tests for various blockchain data providers, NFT marketplaces, DeFi protocols, and cryptocurrency APIs. The test suite ensures proper functionality of API clients, data parsing, error handling, and integration with multiple blockchain networks including Bitcoin, Ethereum, Solana, and others.

## Purpose and Functionality

The test suite validates:
- API endpoint construction and authentication across multiple providers
- Response parsing for balances, transactions, NFT data, and DeFi positions
- Error handling and retry logic for various failure scenarios
- Integration testing with real and mocked API endpoints
- Data transformation from provider-specific formats to standardized models
- Cross-chain compatibility and blockchain-specific features

## Directory Structure

### Core Files

#### `__init__.py`
Empty Python package initialization file.

#### `conftest.py`
Shared pytest configuration providing utility functions:
- `read_json_file()`: Loads JSON test data from files
- `read_file()`: Reads raw file content as strings
- Common test utilities used across all test modules

#### `fake_sleep_provider.py`
Mock implementation of ISleepProvider for testing rate limiting:
- Tracks sleep calls without actually sleeping
- Allows verification of rate limiting behavior
- Used to test API retry and backoff logic

### Blockchain-Specific Test Files

#### Bitcoin and Bitcoin-like Chains
- **`test_blockchair_btc.py`**: Tests Blockchair API for Bitcoin balances and transactions
- **`test_blockchair_doge.py`**: Tests Blockchair API for Dogecoin
- **`test_blockchair_ltc.py`**: Tests Blockchair API for Litecoin
- **`test_trezor_btc.py`**: Tests Trezor's Blockbook API for Bitcoin including xpub support

#### Ethereum and EVM Chains
- **`test_ethplorer.py`**: Tests Ethplorer API for Ethereum token balances
- **`test_optimistic_etherscan.py`**: Tests Etherscan-compatible API for Optimism network

#### Other Blockchains
- **`test_solana.py`**: Comprehensive Solana API tests including token lists and staking
- **`test_cosmos.py`**: Tests for Cosmos blockchain integration
- **`test_subscan_polkadot.py`**: Tests Subscan API for Polkadot balances and staking
- **`test_sui.py`**: Tests for Sui blockchain integration
- **`test_blockchainos.py`**: Tests for Blockchain Operating System (BOS) operations

#### Multi-Source and Specialized Tests
- **`test_multisources.py`**: Tests aggregation across multiple data sources

### Subdirectories

#### `cassettes/`
VCR cassettes for recording/replaying HTTP requests:
- `test_fetch_metaplex_account.yaml`: Metaplex NFT account data
- `test_get_balance.yaml`: Balance fetch recordings
- `test_parse_metaplex_account.yaml`: Metaplex parsing tests

#### `covalenth/`
Covalent API test suite:
- `__init__.py`: Package initialization
- `ethereum.json`: Ethereum balance test data
- `test_ethereum.py`: Covalent Ethereum API tests

#### `data/`
Extensive test data fixtures for all blockchain integrations. See [data/STRUCTURE.md](data/STRUCTURE.md) for detailed information about test data files including responses from Blockchair, Ethplorer, OpenSea, MagicEden, SimpleHash, Solana, and more.

#### `debank/`
Comprehensive DeBank DeFi portfolio tracker tests. See [debank/STRUCTURE.md](debank/STRUCTURE.md) for detailed information about DeBank API testing including balance parsing, portfolio positions, protocol caching, and usage statistics.

#### `nft/`
NFT marketplace API test suite. See [nft/STRUCTURE.md](nft/STRUCTURE.md) for detailed information about NFT API tests including MagicEden, OpenSea, SimpleHash, and UniSat integrations.

#### `perpetual/`
Perpetual Protocol integration tests:
- `__init__.py`: Package initialization
- `test_perpetual.py`: Tests for PERP token contract interactions and balance fetching

#### `synthetix/`
Synthetix protocol integration tests:
- `__init__.py`: Package initialization
- `cassettes/test_synthetix_optimism_api.yaml`: Recorded Optimism API responses
- `data/contracts.md`: Synthetix contract addresses and documentation
- `test_synthetix.py`: Synthetix staking and rewards tests

## Key Testing Patterns

### Fixture Usage
- Heavy use of pytest fixtures for reusable test data and API clients
- JSON response data loaded from files for predictable testing
- Shared fixtures in conftest.py files at multiple levels

### Mocking Strategies
- `requests_mock` for HTTP request mocking in unit tests
- VCR cassettes for recording/replaying real API interactions
- `FakeSleepProvider` for testing rate limiting without delays

### Integration Testing
- Tests marked with `@pytest.mark.integration` require real API access
- Integration tests often skipped in CI but used for validation
- Separate test data saved from real API responses

### Error Handling
- Comprehensive testing of error responses and edge cases
- Validation of retry logic and backoff strategies
- Testing of malformed data and unknown blockchain handling

## Important Conventions

### Test Organization
- One test file per API integration or blockchain
- Fixtures defined in conftest.py files for reusability
- Test data stored as JSON files in data/ directories
- Clear separation between unit and integration tests

### Data Validation
- All monetary values use `Decimal` for precision
- Timezone-aware datetime parsing (UTC standard)
- Address validation and checksum verification
- Consistent blockchain and coin identification

### API Testing Standards
- Mock all external HTTP requests in unit tests
- Test both successful responses and error conditions
- Validate complete data transformation pipeline
- Ensure backward compatibility with API changes

## Dependencies and Integration Points

The test suite integrates with:
- Multiple blockchain APIs (Blockchair, Ethplorer, Subscan, etc.)
- NFT marketplaces (OpenSea, MagicEden, SimpleHash, UniSat)
- DeFi protocols (DeBank, Synthetix, Perpetual)
- Standard pytest testing framework and fixtures
- blockapi v2 models and coin definitions
- HTTP mocking libraries (requests_mock, vcrpy)

## Usage

Run tests with pytest:
```bash
# Run all tests
pytest test/v2/api/

# Run specific test file
pytest test/v2/api/test_solana.py

# Run only unit tests (skip integration)
pytest test/v2/api/ -m "not integration"

# Run with coverage
pytest test/v2/api/ --cov=blockapi.v2.api
```