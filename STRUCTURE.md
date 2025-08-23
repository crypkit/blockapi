# Blockapi Library

## Overview

Blockapi is a comprehensive Python library that provides a unified interface for interacting with blockchain APIs, cryptocurrency data providers, and NFT marketplaces. As a critical component of the Crypkit platform, it abstracts the complexity of integrating with 50+ blockchain networks through both legacy (v1) and modern (v2) implementations, handling everything from simple balance queries to complex DeFi portfolio analysis and NFT data aggregation.

## Purpose and Architecture

The library serves as a blockchain data abstraction layer that:
- Provides a consistent, unified API across diverse blockchain networks and data providers
- Handles API authentication, rate limiting, retries, and error recovery automatically
- Normalizes heterogeneous data formats from various sources into standardized models
- Supports both basic blockchain operations (balance, transactions) and advanced features (DeFi protocols, NFT marketplaces)
- Maintains backward compatibility through dual-version architecture (v1 legacy, v2 modern)

### Architectural Principles
- **Dynamic API Discovery**: Automatically discovers and uses available APIs without hardcoding
- **Graceful Degradation**: Falls back to alternative APIs when primary ones fail
- **Precision First**: All monetary values use Decimal type for financial accuracy
- **Extensibility**: New blockchains and protocols can be added by implementing standard interfaces

## Directory Structure

```
blockapi/
├── CHANGELOG.md                # Detailed version history and changes
├── LICENSE.md                  # MIT License
├── Makefile                    # Build and test automation
├── README.md                   # User-facing documentation
├── pyproject.toml              # Python project configuration (Black, isort, semantic-release)
├── pytest.ini                  # Pytest configuration with custom markers
├── setup.cfg                   # Package metadata (empty, uses setup.py)
├── setup.py                    # Package installation and dependencies
└── blockapi/                   # Main library package
    ├── STRUCTURE.md            # See blockapi/STRUCTURE.md for library architecture details
    ├── __init__.py             # Core API functions and dynamic discovery
    ├── services.py             # Base service classes and HTTP infrastructure
    ├── test_data.py            # Test addresses and API key management
    ├── test/                   # Comprehensive test suite
    │   └── STRUCTURE.md        # See blockapi/test/STRUCTURE.md for test documentation
    ├── utils/                  # Common utility functions
    │   └── STRUCTURE.md        # See blockapi/utils/STRUCTURE.md for utilities documentation
    └── v2/                     # Modern v2 implementation
        └── STRUCTURE.md        # See blockapi/v2/STRUCTURE.md for v2 architecture
```

## Configuration Files

### `setup.py`
Defines package metadata and dependencies:
- **Version**: 1.3.0 (as of last update)
- **Core Dependencies**: requests, pytz, coinaddrng, web3, pydantic
- **Blockchain-Specific**: solders (Solana), ethereum_input_decoder
- **Utilities**: fake_useragent, beautifulsoup4, lxml
- **Testing**: pytest, pytest-vcr, requests_mock

### `pyproject.toml`
Development tooling configuration:
- **Black**: Line length 88, skip string normalization
- **isort**: Black-compatible profile
- **semantic-release**: Version tracking in setup.py

### `pytest.ini`
Test framework configuration:
- **Markers**: `integration` for tests requiring actual API connections
- **Python Path**: Current directory for imports

### `Makefile`
Development workflow automation:
- `make install`: Install library locally
- `make test`: Run v1 tests
- `make test-v2-api`: Run v2 API tests
- `make dist`: Build and publish to PyPI

## Core Functionality

### Public API (blockapi/__init__.py)
- `get_balance_from_random_api(symbol, address)`: Fetches balance using suitable API
- `get_api_classes_for_coin(symbol)`: Returns all APIs supporting a cryptocurrency
- `get_all_supported_coins()`: Lists all supported cryptocurrency symbols
- `check_address_valid(symbol, address)`: Validates blockchain addresses
- `get_working_apis_for_coin(symbol)`: Tests and returns functional APIs

### Key Components
- **blockapi/**: Core v1 implementation and library entry point - See [blockapi/STRUCTURE.md](blockapi/STRUCTURE.md)
- **blockapi/v2/**: Modern architecture with enhanced features - See [blockapi/v2/STRUCTURE.md](blockapi/v2/STRUCTURE.md)
- **blockapi/utils/**: Shared utilities for address, datetime, and number handling - See [blockapi/utils/STRUCTURE.md](blockapi/utils/STRUCTURE.md)
- **blockapi/test/**: Comprehensive test coverage for both v1 and v2 - See [blockapi/test/STRUCTURE.md](blockapi/test/STRUCTURE.md)

## Supported Blockchains and Features

### Native Blockchain Support (v2)
- **Bitcoin Family**: BTC, LTC, DOGE (via Blockchair, Trezor)
- **Ethereum & L2s**: ETH, Optimism (via Ethplorer, Etherscan)
- **Cosmos Ecosystem**: ATOM, OSMO, DYDX, TIA (via native APIs)
- **Solana**: SOL and SPL tokens (via RPC, Solscan)
- **Polkadot/Kusama**: DOT, KSM (via Subscan)
- **Others**: SUI, Terra, BOS

### Multi-Chain Aggregators
- **DeBank**: 40+ chains with DeFi protocol integration
- **Covalenth**: 15+ EVM chains with unified API
- **SimpleHash**: NFT data across multiple chains

### Specialized Integrations
- **NFT Marketplaces**: OpenSea, Magic Eden, SimpleHash, UniSat
- **DeFi Protocols**: Synthetix, Perpetual Protocol
- **Explorers**: Blockchair, Ethplorer, Subscan, various chain-specific explorers

## Usage Examples

### Basic Balance Query (v1)
```python
import blockapi

# Get Bitcoin balance using random API
balance = blockapi.get_balance_from_random_api('BTC', '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')

# Validate Ethereum address
is_valid = blockapi.check_address_valid('ETH', '0x...')
```

### Advanced Usage (v2)
```python
from blockapi.v2.api import SolanaApi, DebankApi
from blockapi.v2.models import Blockchain

# Native blockchain API
solana = SolanaApi()
balances = solana.get_balance("11111111111111111111111111111111")

# DeFi portfolio aggregation
debank = DebankApi(api_key="YOUR_KEY", is_all=True)
portfolio = debank.get_portfolio("0x...")

# Custom RPC endpoint
from blockapi.v2.api import EthereumApi
eth = EthereumApi(base_url="https://mainnet.infura.io/v3/YOUR_KEY")
```

## Development Workflow

### Installation
```bash
# Development installation
pip install -e .

# Or using make
make install
```

### Testing
```bash
# Run all tests
pytest

# Run v1 tests only
make test

# Run v2 tests only
make test-v2-api

# Skip integration tests
pytest -m "not integration"
```

### Publishing
```bash
# Build and publish to PyPI
make dist
```

## Important Conventions

1. **Symbol Format**: Always uppercase (BTC, ETH, SOL)
2. **Address Validation**: Performed before API calls
3. **Error Handling**: APIs return None on failure rather than raising
4. **Decimal Precision**: All monetary values use Decimal type
5. **API Keys**: Retrieved from environment variables
6. **Rate Limiting**: Automatic throttling based on API limits
7. **Timezone**: All datetime objects use UTC

## Dependencies and Requirements

### Runtime Dependencies
- Python 3.x
- Core: requests, pytz, coinaddrng
- Blockchain-specific: web3, solders, ethereum_input_decoder
- Data modeling: pydantic, attrs
- Utilities: beautifulsoup4, fake_useragent

### Development Dependencies
- Testing: pytest, pytest-vcr, requests_mock
- Formatting: black, isort
- Build: setuptools, twine

## Integration with Crypkit

As documented in the main CLAUDE.md, blockapi serves as the blockchain data layer for Crypkit:
- Used by microservices for balance and transaction data
- Integrated with currencies-module for price correlation
- Provides portfolio data for frontend display
- Enables cross-chain asset tracking

## Future Extensibility

The architecture supports:
- Adding new blockchain APIs by implementing base interfaces
- Extending to new DeFi protocols through standardized models
- Integrating additional NFT marketplaces
- Enhanced caching and WebSocket support
- Cross-chain interoperability features