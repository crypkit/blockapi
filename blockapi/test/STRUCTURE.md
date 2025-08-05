# Blockapi Test Suite

## Overview

This directory contains the comprehensive test suite for the blockapi library, a Python package that provides a unified interface for interacting with various blockchain APIs, cryptocurrency data providers, and NFT marketplaces. The test suite covers both the legacy v1 API and the modern v2 implementation, ensuring robust functionality across multiple blockchain ecosystems.

## Purpose and Functionality

The test suite serves as the quality assurance framework for the blockapi library, validating:
- Core functionality of blockchain API integrations
- Data parsing and normalization across different providers
- Error handling and retry mechanisms
- Address validation and utility functions
- Both legacy (v1) and modern (v2) API implementations

## Directory Structure

### Root Level Test Files

#### `__init__.py`
Empty Python package initialization file that marks this directory as a Python package.

#### `test_blockapi.py`
Core test framework for the blockapi library's main functionality:
- Implements `TestBlockApiProviders` class for automated testing of all supported blockchain APIs
- Tests currency support detection via `get_all_supported_coins()`
- Validates API class discovery with `get_api_classes_for_coin()`
- Performs bulk testing across multiple currencies and addresses
- Provides diagnostic methods for analyzing test results and API performance
- Tests address validation functionality

#### `test_num.py`
Tests for numerical utility functions:
- Validates `decimals_to_raw()` function for converting decimal numbers to raw blockchain values
- Ensures proper handling of decimal precision for cryptocurrency amounts

#### `test_random_user_agent.py`
Tests for user agent randomization functionality:
- Validates the `get_random_user_agent()` utility function
- Ensures proper generation of random user agents for API requests

### Subdirectory

#### `v2/`
The modern v2 API test suite containing comprehensive tests for the latest version of the blockapi library. See [v2/STRUCTURE.md](v2/STRUCTURE.md) for detailed information about:
- Core v2 functionality tests (base classes, models, blockchain mapping)
- Extensive API integration tests for 30+ blockchain providers
- NFT marketplace integration tests
- DeFi protocol integration tests
- Comprehensive test data and mocking infrastructure

## Key Components and Patterns

### Test Infrastructure
- Uses pytest as the primary testing framework
- Leverages test data from `blockapi.test_data` module
- Implements comprehensive API testing across multiple blockchain networks
- Provides diagnostic capabilities for analyzing test results

### Testing Approach
1. **Automated Multi-API Testing**: The `TestBlockApiProviders` class enables bulk testing of all supported APIs
2. **Currency Coverage**: Tests span multiple cryptocurrencies using predefined test addresses
3. **Method Testing**: Supports testing various API methods (default: `get_balance`)
4. **Error Tracking**: Comprehensive error collection and diagnostic reporting

### Data Validation
- Address validation for various blockchain formats
- Decimal precision handling for cryptocurrency amounts
- API response structure validation
- Success/failure tracking for each API provider

## Integration Points

The test suite validates integration with:
- **Core Library Functions**: Address validation, coin support detection, API class discovery
- **Utility Functions**: Numerical conversions, user agent generation
- **V2 API Suite**: Modern implementation with enhanced features and broader blockchain support
- **Test Data Module**: Centralized test addresses and API keys management

## Usage Examples

### Running the Tests
```bash
# Run all tests
pytest test/

# Run only v1 tests (excluding v2)
pytest test/test_*.py

# Run specific test file
pytest test/test_blockapi.py

# Run with verbose output
pytest test/ -v
```

### Using TestBlockApiProviders
```python
# Initialize test framework
tester = TestBlockApiProviders()

# Run automated tests for all supported currencies
tester.run_all()

# Get diagnostic information
diagnostics = tester.get_diagnostic()

# Custom test data
custom_data = [
    {
        'currency': 'BTC',
        'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        'value': '50'
    }
]
tester.data = custom_data
tester.run()
```

## Important Conventions

### Test Organization
- V1 tests remain at the root level for backward compatibility
- V2 tests are isolated in the `v2/` subdirectory
- Clear separation between unit tests and integration tests
- Comprehensive error handling and reporting

### Code Quality Standards
- All tests should be deterministic and reproducible
- External API calls should be mocked where appropriate
- Test both success and failure scenarios
- Maintain clear test naming conventions

## Dependencies

The test suite requires:
- pytest and related testing utilities
- blockapi library (both v1 and v2)
- Test data module with predefined addresses and API keys
- Various mocking and fixture libraries (see v2/STRUCTURE.md for v2-specific dependencies)

## Future Considerations

The test suite architecture supports:
- Easy addition of new blockchain API providers
- Extension of test methods beyond balance checking
- Integration of new cryptocurrency protocols
- Backward compatibility with legacy v1 implementations while promoting v2 adoption