# Blockapi Library Structure

## Overview

The blockapi library is a comprehensive Python package that provides a unified interface for interacting with various blockchain APIs, cryptocurrency data providers, and NFT marketplaces. It serves as a critical component of the Crypkit platform, enabling seamless integration with over 50 blockchain networks through both legacy (v1) and modern (v2) implementations.

## Purpose and Architecture

This library abstracts the complexity of interacting with different blockchain explorers, APIs, and data providers by:
- Providing a consistent interface across multiple blockchain networks
- Handling rate limiting, retries, and error recovery
- Normalizing data formats from various sources
- Supporting both simple balance queries and complex DeFi portfolio analysis
- Integrating NFT marketplace data from multiple providers

The library follows a dual-version architecture:
- **v1 (Legacy)**: Original implementation with basic blockchain API support
- **v2 (Modern)**: Enhanced architecture with standardized models, better error handling, and expanded protocol support

## Directory Structure

```
blockapi/
├── __init__.py              # Package initialization with core functions and COINS mapping
├── services.py              # Base service classes and API infrastructure
├── test_data.py             # Test addresses and API key management
├── test/                    # Comprehensive test suite
│   └── STRUCTURE.md         # See test/STRUCTURE.md for detailed test documentation
├── utils/                   # Utility functions for common operations
│   └── STRUCTURE.md         # See utils/STRUCTURE.md for utility details
└── v2/                      # Modern v2 implementation
    └── STRUCTURE.md         # See v2/STRUCTURE.md for v2 architecture details
```

## Core Files

### `__init__.py`
The main entry point for the blockapi library, providing:

**Core Functions:**
- `get_balance_from_random_api(symbol, address)`: Fetches balance using a random suitable API
- `get_api_classes_for_coin(symbol)`: Returns all API classes supporting a specific cryptocurrency
- `get_all_supported_coins()`: Lists all supported cryptocurrency symbols
- `check_address_valid(symbol, address)`: Validates blockchain addresses using coinaddrng
- `get_working_apis_for_coin(symbol)`: Tests and returns functional APIs for a coin

**Key Features:**
- Dynamic API class discovery through inheritance inspection
- Automatic API selection based on address type (regular/xpub) and network (mainnet/testnet)
- Built-in retry logic with fallback to alternative APIs
- Test mode support for validating API functionality

**COINS Dictionary:**
Maps CoinGecko IDs to standard symbols for 25+ major cryptocurrencies (BTC, ETH, SOL, etc.)

### `services.py`
Foundation classes for all blockchain API implementations:

**Core Classes:**
- `Service`: Base class for HTTP-based API services
  - Cloudflare bypass support
  - Rate limiting with configurable delays
  - Automatic error response handling
  - Session management for request reuse

- `BlockchainInterface`: Abstract interface defining blockchain API contract
  - `get_balance()`: Required method for balance retrieval
  - `get_txs()`: Optional transaction history retrieval
  - Pagination support with offset/limit parameters

- `BlockchainAPI`: Combined Service + BlockchainInterface base
  - Automatic network detection (mainnet/testnet)
  - Address validation integration
  - Decimal conversion utilities

**Decorators:**
- `@set_default_args_values`: Automatically applies default pagination values
- `@on_failure_return_none()`: Graceful error handling decorator

**Exception Types:**
- `APIError`: Base exception for all API errors
- `AddressNotExist`: Invalid or non-existent address
- `APIKeyMissing`: Required API key not provided
- `InternalServerError`, `BadGateway`, `GatewayTimeOut`: HTTP error wrappers

### `test_data.py`
Centralized test data management:

**Test Addresses Dictionary:**
- Contains valid test addresses for 45+ cryptocurrencies
- Includes regular addresses, xpub keys, and contract addresses
- Used for automated API testing and validation

**API Key Management:**
- `get_test_api_key(api_cls_name)`: Retrieves API keys from environment variables
- Supports custom naming patterns (e.g., CRYPTOIDAPI_KEY)

## Subdirectories

### `test/`
Comprehensive test suite for both v1 and v2 implementations. See [test/STRUCTURE.md](test/STRUCTURE.md) for:
- Core functionality tests
- Multi-API automated testing framework
- Address validation tests
- Utility function tests
- Complete v2 API test coverage

### `utils/`
Common utility functions used throughout the library. See [utils/STRUCTURE.md](utils/STRUCTURE.md) for:
- Address validation and checksum formatting
- DateTime parsing for blockchain timestamps
- Decimal/raw value conversions for precise cryptocurrency calculations
- User agent randomization for API requests

### `v2/`
Modern implementation with enhanced architecture. See [v2/STRUCTURE.md](v2/STRUCTURE.md) for:
- Standardized data models and interfaces
- 50+ blockchain API implementations
- DeFi protocol integrations (Synthetix, Perpetual)
- NFT marketplace support (OpenSea, Magic Eden, etc.)
- Multi-chain aggregators (DeBank, Covalenth)

## Integration Patterns

### Basic Usage (v1)
```python
import blockapi

# Get balance for Bitcoin address
balance = blockapi.get_balance_from_random_api('BTC', '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')

# Get all APIs supporting Ethereum
eth_apis = blockapi.get_api_classes_for_coin('ETH')

# Validate address
is_valid = blockapi.check_address_valid('BTC', 'invalid_address')
```

### Direct API Usage (v1)
```python
# Use specific API class
from blockapi.v1.blockchain_info import BlockchainInfo

api = BlockchainInfo('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')
balance = api.get_balance()
transactions = api.get_txs(limit=10)
```

### Modern Usage (v2)
```python
from blockapi.v2.api import SolanaApi, DebankApi
from blockapi.v2.models import Blockchain

# Native blockchain API
solana = SolanaApi()
balances = solana.get_balance("11111111111111111111111111111111")

# Multi-chain aggregator
debank = DebankApi(api_key="YOUR_KEY")
portfolio = debank.get_portfolio("0x...")
```

## Key Design Decisions

1. **Dual Version Support**: Maintains backward compatibility while introducing modern features
2. **Dynamic API Discovery**: Automatically finds and uses available APIs without hardcoding
3. **Graceful Degradation**: Falls back to alternative APIs when primary ones fail
4. **Address Validation**: Validates addresses before making API calls to prevent errors
5. **Decimal Precision**: All monetary values use Decimal type for accuracy
6. **Testability**: Comprehensive test suite with real blockchain data

## Dependencies

### Core Dependencies
- `requests`: HTTP client for API calls
- `cfscrape`: Cloudflare bypass for protected APIs
- `coinaddrng`: Multi-blockchain address validation

### v2 Additional Dependencies
- `attrs`, `pydantic`: Data modeling and validation
- `web3`, `solders`: Blockchain-specific libraries
- `eth_utils`: Ethereum utilities
- Various protocol-specific SDKs

## Important Conventions

1. **Symbol Format**: Always use uppercase symbols (BTC, ETH, SOL)
2. **Address Format**: Blockchain-specific, validated before use
3. **Error Handling**: APIs return None on failure rather than raising exceptions
4. **API Keys**: Retrieved from environment variables for security
5. **Rate Limiting**: Respect API rate limits through built-in delays

## Future Considerations

The library architecture supports:
- Easy addition of new blockchain APIs
- Extension to new DeFi protocols
- Integration of additional NFT marketplaces
- Enhanced caching mechanisms
- WebSocket support for real-time data