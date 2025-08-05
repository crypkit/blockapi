# Covalenth API Integration

## Overview

This directory contains the Covalenth API integration for the blockapi library. Covalenth (formerly Covalent) is a unified blockchain data API that provides access to balance and token information across multiple blockchain networks. The implementation follows a consistent pattern where each blockchain has its own module that inherits from a common base class.

## Architecture

The directory implements a clean inheritance pattern where:
- `base.py` contains the abstract base class with core functionality
- Each blockchain-specific file extends the base class with chain-specific configuration
- All implementations share the same API structure and authentication mechanism

## Files and Purpose

### Core Implementation

- **`__init__.py`**: Empty initialization file for the Python package

- **`base.py`**: Abstract base class that implements the core Covalenth API functionality
  - Defines `CovalentApiBase` class that extends `BlockchainApi` and implements `IBalance`
  - Implements HTTP Basic authentication using the API key
  - Provides `get_balance()` method to fetch token balances for an address
  - Handles response parsing and converts raw data to standardized `BalanceItem` objects
  - Includes checksum address validation for EVM-compatible chains
  - Filters out zero-balance tokens
  - Supports ERC token standards detection

### Blockchain-Specific Implementations

Each blockchain implementation follows the same pattern, defining:
- `CHAIN_ID`: The unique chain identifier used by Covalenth
- `api_options`: Configuration object with blockchain type, base URL, and rate limits
- `coin`: The native coin/token for that blockchain

#### EVM-Compatible Chains

- **`ethereum.py`**: Ethereum mainnet (Chain ID: 1, Native coin: ETH)
- **`binance_smart_chain.py`**: BSC/BNB Chain (Chain ID: 56, Native coin: BNB)
- **`polygon.py`**: Polygon/Matic network (Chain ID: 137, Native coin: MATIC)
- **`avalanche.py`**: Avalanche C-Chain (Chain ID: 43114, Native coin: AVAX)
- **`arbitrum.py`**: Arbitrum One (Chain ID: 42161, Native coin: ETH)
- **`fantom.py`**: Fantom Opera (Chain ID: 250, Native coin: FTM)
- **`heco.py`**: Huobi ECO Chain (Chain ID: 128, Native coin: HT)
- **`moonbeam.py`**: Moonbeam on Polkadot (Chain ID: 1284, Native coin: GLMR)
- **`base.py`**: Base network (Chain ID: 8453, Native coin: ETH)

#### Other Blockchain Networks

- **`astar.py`**: Astar Network (Chain ID: 592, Native coin: ASTR)
- **`axie.py`**: Axie Infinity's Ronin chain (Chain ID: 2020, Native coin: RON)
- **`iotex.py`**: IoTeX network (Chain ID: 4689, Native coin: IOTX)
- **`klaytn.py`**: Klaytn network (Chain ID: 8217, Native coin: KLAY)
- **`palm.py`**: Palm network (Chain ID: 11297108109, Native coin: PALM)
- **`rsk.py`**: RSK (Rootstock) network (Chain ID: 30, Native coin: RBTC)

## Key Features

1. **Unified API Interface**: All blockchain implementations expose the same `get_balance()` method
2. **Automatic Token Detection**: Discovers and returns all tokens held by an address
3. **Native Coin Handling**: Properly distinguishes between native blockchain coins and tokens
4. **Rate Limiting**: Built-in rate limiting (0.2 requests per second) to respect API limits
5. **Error Handling**: Graceful error handling with logging for debugging
6. **Token Metadata**: Retrieves token names, symbols, decimals, logos, and supported standards

## Integration Points

- Inherits from `blockapi.v2.base.BlockchainApi` for common blockchain API functionality
- Uses standardized models from `blockapi.v2.models` (BalanceItem, Coin, CoinInfo)
- References native coins from `blockapi.v2.coins` module
- Implements the `IBalance` interface for balance-fetching capabilities

## API Usage Pattern

All implementations follow this pattern:
```python
api = SpecificBlockchainCovalentApi(api_key="your_key")
balances = api.get_balance(address="0x...")
```

The returned `balances` list contains `BalanceItem` objects with:
- Token balance (raw and formatted)
- Coin information (symbol, name, decimals, contract address)
- Metadata (logo URL, supported standards)
- Last transfer timestamp

## Dependencies

- `eth_utils`: For EVM address checksum validation
- `logging`: For debug and error logging
- Standard blockapi v2 modules for base classes and models