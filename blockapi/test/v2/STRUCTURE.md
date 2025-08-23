# Blockapi V2 Test Suite

## Overview

This directory contains the comprehensive test suite for the blockapi v2 library, which provides a unified interface for interacting with various blockchain APIs, NFT marketplaces, and DeFi protocols. The test suite validates the core functionality of the library including API integrations, data parsing, error handling, and cross-chain compatibility.

## Purpose and Functionality

The v2 test suite serves as the quality assurance framework for the blockapi library, ensuring:
- Reliable integration with 30+ blockchain data providers and APIs
- Correct parsing and normalization of diverse API response formats
- Robust error handling and retry mechanisms
- Comprehensive coverage of blockchain-specific features and edge cases
- Validation of core models and base classes used throughout the library

## Directory Structure

### Core Test Files

#### `__init__.py`
Empty Python package initialization file.

#### `test_base.py`
Tests for the `CustomizableBlockchainApi` base class that all API implementations inherit from:
- Connection error handling with automatic retries
- HTTP status code handling (401, 500, etc.)
- Retry logic for transient failures
- Exception handling and error response formatting
- Integration with custom sleep providers for rate limiting

#### `test_blockchain_api.py`
Validates the blockchain API base class implementation:
- Tests that subclasses must implement required methods
- Ensures proper API options configuration
- Validates blockchain assignment to API instances

#### `test_blockchain_mapping.py`
Tests for blockchain identifier mapping and resolution:
- Chain ID to blockchain enum mapping
- Blockchain name standardization
- Cross-reference validation between different naming conventions

#### `test_data.py`
Core data model and parsing tests:
- JSON response parsing utilities
- Data transformation helpers
- Common test data fixtures

#### `test_enumerate_classes.py`
Tests for dynamic class enumeration and discovery:
- API class auto-discovery mechanisms
- Plugin system validation
- Dynamic import verification

#### `test_generic.py`
Generic functionality tests that don't fit specific categories:
- Utility function testing
- Helper method validation
- Cross-cutting concerns

#### `test_models.py`
Tests for core v2 data models:
- `Protocol` model creation and validation
- `BalanceItem` with protocol associations
- Model serialization and deserialization
- Decimal precision handling for financial data

### Subdirectories

#### `api/`
The main API integration test suite containing tests for all blockchain data providers. See [api/STRUCTURE.md](api/STRUCTURE.md) for comprehensive details about:
- Individual blockchain API tests (Bitcoin, Ethereum, Solana, etc.)
- NFT marketplace integrations (OpenSea, MagicEden, SimpleHash, UniSat)
- DeFi protocol tests (DeBank, Synthetix, Perpetual)
- Extensive test data fixtures and mocking infrastructure

## Key Testing Patterns

### Test Organization
- Hierarchical structure mirroring the library's module organization
- Separation of unit tests from integration tests
- Comprehensive fixtures defined in conftest.py files
- Test data stored as JSON files for reproducibility

### Mocking and Fixtures
- `FakeSleepProvider` for testing rate limiting without delays
- `requests_mock` for HTTP request interception
- VCR cassettes for recording/replaying API interactions
- Shared fixtures cascading through conftest.py hierarchy

### Error Handling Tests
- Connection error retry logic validation
- HTTP status code handling (4xx, 5xx responses)
- Malformed response parsing
- Unknown blockchain/protocol handling
- API authentication failures

### Data Validation
- Decimal precision for all monetary values
- UTC timezone consistency for timestamps
- Address checksum verification
- Blockchain and token identification accuracy

## Integration Points

The test suite validates integration with:
- **30+ Blockchain APIs**: Including Blockchair, Ethplorer, Subscan, Trezor, and more
- **NFT Marketplaces**: OpenSea, MagicEden, SimpleHash, UniSat
- **DeFi Protocols**: DeBank portfolio tracker, Synthetix, Perpetual Protocol
- **Multiple Blockchains**: Bitcoin, Ethereum, Solana, Polkadot, Cosmos, Sui, and others
- **Core Libraries**: pytest, requests, Decimal, datetime with timezone support

## Important Conventions

### Testing Standards
- All external API calls must be mocked in unit tests
- Integration tests marked with `@pytest.mark.integration`
- Test both success and failure scenarios
- Validate complete data transformation pipelines
- Ensure backward compatibility

### Code Quality
- Comprehensive test coverage expected
- Clear test naming following `test_<functionality>` pattern
- Extensive use of fixtures for DRY principles
- Detailed docstrings for complex test scenarios

### Performance Considerations
- Rate limiting tested without actual delays
- Batch operations validated for efficiency
- Caching mechanisms verified (e.g., DeBank protocol cache)
- Pagination handling for large result sets

## Usage

Run the test suite using pytest:
```bash
# Run all v2 tests
pytest test/v2/

# Run with coverage report
pytest test/v2/ --cov=blockapi.v2

# Run only unit tests (skip integration)
pytest test/v2/ -m "not integration"

# Run specific test module
pytest test/v2/test_models.py

# Run with verbose output
pytest test/v2/ -v
```

## Dependencies

The test suite requires:
- pytest and related plugins (pytest-cov, pytest-mock)
- requests-mock for HTTP mocking
- vcrpy for recording API interactions
- Core blockapi v2 library and all its dependencies
- Test data files in JSON format