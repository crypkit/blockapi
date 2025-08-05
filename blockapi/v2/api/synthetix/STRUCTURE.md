# Synthetix API Integration

## Overview

This directory contains the blockchain API integration for Synthetix, a decentralized synthetic asset issuance protocol built on Ethereum and Optimism. The integration allows fetching balances, staking information, rewards, and collateralization data for Synthetix users across both Ethereum mainnet and Optimism L2.

## Directory Structure

```
synthetix/
├── __init__.py          # Module exports and public API
├── synthetix.py         # Core implementation of Synthetix API
└── synthetix_abi.py     # Smart contract ABI definitions
```

## Files and Components

### `__init__.py`
Exports the main API classes and utility functions for external use:
- `SynthetixApi` - Base abstract class for Synthetix integrations
- `SynthetixMainnetApi` - Ethereum mainnet implementation
- `SynthetixOptimismApi` - Optimism L2 implementation  
- `snx_contract_address` - Contract address resolver for mainnet
- `snx_optimism_contract_address` - Contract address resolver for Optimism

### `synthetix.py`
Core implementation containing:

**Key Classes:**
- `SynthetixApi` - Abstract base class implementing `CustomizableBlockchainApi` and `IBalance`
  - Handles SNX token balances, staking positions, debt, rewards, and vesting
  - Supports both Ethereum mainnet and Optimism L2 networks
- `SynthetixMainnetApi` - Ethereum mainnet-specific implementation
- `SynthetixOptimismApi` - Optimism L2-specific implementation

**Data Types:**
- `CollateralizationStats` - Collateralization ratio information
- `WeeklyReward` - Exchange and staking rewards structure
- `Staking` - Complete staking position including collateral, debt, rewards
- `Synth` - Synthetic asset metadata (symbol and contract address)

**Key Functions:**
- `snx_contract_address()` - Dynamically resolves Synthetix contract names to addresses
- `snx_optimism_contract_address()` - Optimism-specific contract resolver using GitHub docs

**Core Functionality:**
- Balance fetching for SNX and synthetic assets (sUSD, etc.)
- Staking information retrieval including:
  - Transferable (unlocked) SNX
  - Total debt owed in sUSD
  - Staked/collateral amounts
  - Vesting/escrowed SNX
  - Weekly rewards (exchange fees and staking rewards)
  - Liquidation rewards
  - Collateralization ratios
- Support for multiple asset types: AVAILABLE, STAKED, DEBT, REWARDS, PRICED_VESTING, LIQUIDATION_REWARDS

### `synthetix_abi.py`
Contains Ethereum smart contract ABI definitions for interacting with Synthetix contracts:
- `synthetix_abi` - Main Synthetix contract ABI
- `feepool_abi` - Fee pool contract for rewards distribution
- `exchangerates_abi` - Exchange rates oracle contract
- `system_settings_abi` - System configuration parameters
- `erc20_abi` - Standard ERC20 token interface
- `rewards_escrow_v2_abi` - Vesting/escrow contract for SNX rewards
- `liquidator_rewards_abi` - Liquidation rewards contract

## Integration Architecture

The Synthetix integration follows the blockapi v2 pattern:
1. Inherits from `CustomizableBlockchainApi` for standardized blockchain API structure
2. Implements `IBalance` interface for balance fetching capabilities
3. Uses Web3.py for direct smart contract interactions
4. Leverages caching (`@lru_cache`) for expensive contract calls
5. Supports multiple networks through polymorphic design

## Key Dependencies

- `web3` - Ethereum blockchain interaction
- `requests` - HTTP requests for contract address resolution
- `beautifulsoup4` - HTML parsing for Optimism contract addresses
- `marko` - Markdown parsing for documentation scraping
- Parent blockapi modules:
  - `blockapi.v2.base` - Base classes and interfaces
  - `blockapi.v2.api.web3_utils` - Web3 utility functions
  - `blockapi.utils.num` - Decimal conversion utilities

## Usage Pattern

The API is designed to be instantiated with a network type and API URL:
```python
# Mainnet
api = SynthetixMainnetApi(api_url="https://mainnet.infura.io/v3/...")

# Optimism
api = SynthetixOptimismApi(api_url="https://optimism-mainnet.infura.io/v3/...")

# Fetch all balances
balances = api.get_balance("0x...address...")
```

## Important Implementation Details

1. **Contract Address Resolution**: Uses dynamic resolution via synthetix.io redirect URLs for mainnet and GitHub markdown parsing for Optimism
2. **Balance Types**: Distinguishes between transferable, staked, vesting, debt, and reward balances
3. **Collateralization**: Calculates collateralization ratios and staking amounts based on system issuance ratios
4. **Decimal Handling**: All amounts use 18 decimal precision consistent with SNX token
5. **Error Handling**: Raises `ValueError` when contracts cannot be found