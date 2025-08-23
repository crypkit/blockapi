# DeBank API Test Suite

## Overview

This directory contains the comprehensive test suite for the DeBank API integration within the blockapi library. DeBank is a Web3 portfolio tracker that provides detailed information about DeFi positions, token balances, and protocol interactions across multiple blockchain networks. The tests ensure proper functionality of API client implementation, data parsing, caching mechanisms, and error handling.

## Purpose and Functionality

The test suite validates the complete DeBank integration including:
- API endpoint construction and authentication
- Response parsing for balances, portfolios, protocols, and chains
- Protocol caching mechanisms for performance optimization
- Error handling for invalid responses and edge cases
- Integration testing with real API endpoints
- Comprehensive unit testing of parsers and models

## File Descriptions

### conftest.py
Pytest configuration and shared fixtures for the DeBank test suite. Provides:
- API client fixtures with different configurations (all tokens on/off)
- Parser fixtures for balance, portfolio, protocol, and usage parsing
- Mock response fixtures loaded from test data files
- Sample data fixtures for testing specific scenarios
- Protocol cache fixtures for testing caching behavior
- Chain and protocol model fixtures

### test_debank.py
Core API client tests covering:
- URL building for different endpoints (balance, portfolio, protocols, chains)
- API key authentication in request headers
- Error response handling and logging
- Protocol fetching and caching integration
- Chain data retrieval
- Shared protocol cache across API instances
- Usage statistics retrieval

### test_debank_balance_parser.py
Balance parser testing including:
- Token balance parsing from API responses
- Coin identification and mapping to internal models
- Protocol association with tokens
- Handling of zero balances and empty responses
- Chain-specific token mapping (ETH on different chains)
- Unknown chain handling
- Decimal precision and amount calculations
- Time parsing for last updated timestamps

### test_debank_fetch.py
Integration tests for real API calls (marked with `@pytest.mark.integration`):
- Fetching actual balance data from DeBank API
- Retrieving portfolio positions for test addresses
- Fetching protocol and chain lists
- Saving fetched data for future test reference
- Usage statistics retrieval testing

### test_debank_portfolio_parser.py
Portfolio/pool parsing tests covering:
- Complex DeFi position parsing (lending, borrowing, staking, liquidity)
- Asset type classification and mapping
- Position metadata extraction (health rates, lock times)
- Pool information parsing (IDs, names, tokens)
- Handling duplicate assets
- Unknown chain portfolio handling
- Vesting and time-locked position parsing
- Error handling for malformed data

### test_debank_protocol_cache.py
Protocol cache functionality tests:
- Cache timeout behavior (3600 seconds)
- Cache update detection
- Protocol retrieval from cache
- Cache invalidation and refresh logic
- Efficient protocol data storage

### test_debank_protocol_parser.py
Protocol parser testing for:
- Protocol metadata extraction (ID, name, chain)
- TVL (Total Value Locked) parsing
- Logo and site URL extraction
- Portfolio support flag parsing
- Protocol-to-blockchain mapping

### test_debank_usage_parser.py
API usage statistics parser tests:
- Balance parsing (remaining API credits)
- Daily usage statistics extraction
- Historical usage data parsing
- Date formatting and timezone handling

### test_pool.py
Pool model functionality tests:
- Pool item aggregation
- Balance item appending to pools
- Pool metadata preservation
- Protocol association with pools

### data/
Test data directory containing JSON fixtures for various API responses. See [data/STRUCTURE.md](data/STRUCTURE.md) for detailed information about each test data file and its purpose.

## Key Testing Patterns

### Fixture Usage
- Heavy use of pytest fixtures for reusable test data
- Fixtures cascade from conftest.py to provide consistent test environment
- Mock responses loaded from JSON files for predictable testing

### Parser Testing Strategy
- Each parser (balance, portfolio, protocol, usage) has dedicated test file
- Tests cover both successful parsing and error conditions
- Edge cases like empty responses, unknown chains, and malformed data

### Integration Points
- `requests_mock` for mocking HTTP requests in unit tests
- Real API calls in integration tests (requires API key)
- Protocol cache shared across test instances
- Parser chain: fetch → parse → model conversion

## Important Conventions

### Test Organization
- Unit tests run without external dependencies
- Integration tests marked with `@pytest.mark.integration`
- Test data stored as JSON files in data/ subdirectory
- Fixtures defined in conftest.py for reusability

### Error Testing
- Comprehensive error response testing
- Logging verification with `caplog` fixture
- Unknown chain and protocol handling
- Malformed response handling

### Data Validation
- Decimal precision testing for financial amounts
- Timezone-aware datetime parsing
- Address checksum validation
- Chain ID to blockchain mapping verification

## Dependencies and Integration

The test suite integrates with:
- DeBank Pro API (requires API key for integration tests)
- blockapi v2 models and coin definitions
- Protocol caching system for performance
- Multiple blockchain definitions and mappings
- Decimal and datetime libraries for precise financial data