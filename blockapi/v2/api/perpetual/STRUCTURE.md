# Perpetual Protocol API Integration

## Overview

This directory contains the integration layer for Perpetual Protocol (PERP), a decentralized perpetual futures exchange. The implementation focuses on fetching and parsing staking rewards, vesting rewards, and claimable balances from the Perpetual Protocol's smart contracts and off-chain storage.

## Files

### `__init__.py`
Simple module initialization file that exports the main API class and utility functions:
- Exports `PerpetualApi` - the main API class for interacting with Perpetual Protocol
- Exports `perp_contract_address` - utility function to retrieve contract addresses

### `perp_abi.py`
Contains the Ethereum smart contract ABI (Application Binary Interface) for the rewards contract:
- Defines `rewards_abi` - a comprehensive ABI for the MerkleRedeem contract
- Includes functions for claiming rewards, verifying claims, and managing merkle roots
- Key functions include:
  - `claimWeek` / `claimWeeks` - for claiming rewards for specific periods
  - `claimStatus` - check claim status for a liquidity provider
  - `verifyClaim` - verify merkle proof for reward claims
  - `seedAllocations` - admin function for setting up weekly allocations

### `perpetual.py`
The main implementation file containing all business logic for interacting with Perpetual Protocol:

#### Key Components:

1. **Utility Functions**:
   - `perp_contract_address()` - Retrieves contract addresses for PERP, sPERP, staking rewards, and vesting rewards
   - `perp_contracts()` - Fetches contract metadata from Perpetual Protocol's metadata API

2. **PerpOffChainStorage Class**:
   - Handles interaction with AWS S3-hosted off-chain storage
   - Methods:
     - `get_epoch_snapshots()` - Fetches weekly snapshots for immediate or vesting rewards
     - `get_rewards()` - Retrieves detailed reward data for a specific epoch

3. **PerpProtocol Class**:
   - Core protocol interaction logic
   - Handles reward calculations and claim status checks
   - Methods:
     - `fetch()` - Main entry point returning all reward types
     - `_fetch_staking_claimable_rewards()` - Gets immediately claimable staking rewards
     - `_fetch_staking_vesting_rewards()` - Gets both claimable and locked vesting rewards
     - `_fetch_non_claimed_snapshots()` - Filters out already claimed rewards
     - `_get_total_reward()` - Aggregates rewards across multiple epochs

4. **PerpetualApi Class**:
   - Extends `CustomizableBlockchainApi` and `BalanceMixin`
   - Implements the standard blockapi interface
   - Methods:
     - `fetch_balances()` - Fetches all reward balances for an address
     - `parse_balances()` - Converts raw data to standardized BalanceItem objects
     - `yield_balances()` - Generates balance items for claimable and vesting amounts

## Architecture Patterns

### Data Flow
1. API calls start with `PerpetualApi.fetch_balances()`
2. Creates a `PerpProtocol` instance to handle the actual data fetching
3. Retrieves snapshots from off-chain storage (AWS S3)
4. Checks on-chain claim status via Web3 smart contract calls
5. Calculates unclaimed rewards by cross-referencing snapshots with claim status
6. Returns standardized balance data

### Key Dependencies
- **web3.py** - For Ethereum blockchain interactions
- **requests** - For HTTP calls to metadata and S3 endpoints
- **blockapi.v2.base** - Base classes for API implementation
- **blockapi.v2.coins** - Coin definitions (COIN_PERP)
- **blockapi.v2.models** - Data models for balances and results

### Integration Points
- **Perpetual Protocol Metadata API**: `https://metadata.perp.exchange/production.json`
- **AWS S3 Storage**: `https://s3.amazonaws.com/staking.perp.fi/production`
- **Ethereum Smart Contracts**:
  - Staking Rewards: `0xc2a9e84D77f4B534F049b593C282c5c91F24808A`
  - Vesting Rewards: `0x49a4B8431Fc24BE4b22Fb07D1683E2c52bC56088`

## Important Notes

1. **Caching**: The implementation uses `@lru_cache` decorators to cache contract metadata and reward data, reducing API calls
2. **Reward Types**: Handles three types of rewards:
   - Immediately claimable staking rewards
   - Claimable vesting rewards (past redemption date)
   - Locked vesting rewards (future redemption date)
3. **Merkle Proof System**: The protocol uses merkle trees for efficient reward distribution verification
4. **Time-based Logic**: Vesting rewards become claimable after their `redeemableUntil` timestamp passes