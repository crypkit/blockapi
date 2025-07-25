# DeBank API Test Data

## Overview

This directory contains JSON test data files used for testing the DeBank API integration within the blockapi library. DeBank is a Web3 portfolio tracker that provides comprehensive DeFi data across multiple blockchain networks. These test fixtures represent various API responses from DeBank's endpoints, including portfolio positions, token balances, and protocol interactions.

## Purpose and Functionality

The test data serves as mock responses for unit testing the DeBank API client implementation, ensuring proper parsing and handling of:
- DeFi protocol portfolio positions
- Token balance responses  
- Error conditions and edge cases
- Complex nested data structures from various DeFi protocols

## File Descriptions

### aave_portfolio_response.json
Contains a sample response from the Aave V2 lending protocol showing:
- Staked AAVE positions with rewards
- Lending positions (supplied MKR tokens)
- Asset values, APY calculations, and health rates
- Demonstrates the structure for lending/borrowing protocol responses

### balance_response.json
A comprehensive token balance response showing:
- Multiple token holdings across different chains (Ethereum, BSC, Polygon, Fantom, HECO)
- Token metadata including decimals, logos, prices, and amounts
- Both verified and unverified tokens
- Native chain tokens (ETH, BNB) and ERC-20/BEP-20 tokens

### bio_pools.json
Portfolio data for the BIO protocol featuring:
- Multiple vesting positions with different indices
- Token amounts, claimable amounts, and vesting end dates
- Demonstrates handling of time-locked/vesting token positions
- Shows negative amounts in asset lists (representing locked tokens)

### complex_portfolio_response.json
A large, multi-protocol portfolio response containing:
- Positions across multiple DeFi protocols (Trader Joe, Badger DAO, Bao Finance)
- Various position types: lending, staking, liquidity pools, rewards
- Complex nested structures with supply/borrow token lists
- Demonstrates real-world portfolio complexity

### duplicates.json
Test data for handling duplicate entries, containing:
- Multiple protocol entries with similar structure
- Used to test deduplication logic and data aggregation
- Shows lending positions and locked token scenarios

### esgmx_portfolio_response.json
GMX protocol positions on Arbitrum showing:
- Escrowed GMX (esGMX) staking and vesting
- Multiple reward tokens (GMX, esGMX, ETH)
- Complex staking mechanics with different pool IDs
- Demonstrates handling of escrowed/locked governance tokens

### mist_response.json
A simple token balance response for MIST (Alchemist) token:
- Single token entry with full metadata
- Shows minimal response structure
- Useful for testing basic token parsing

### position_index_portfolio_response.json
Uniswap V3 liquidity positions demonstrating:
- Multiple liquidity positions with position indices
- Token pair pools (PRIME/ETH)
- Supply and reward token lists
- Position-specific metadata and pool information

### tokenset_portfolio_response.json
TokenSets investment positions showing:
- Leveraged token products (BTC2x-FLI, ETH2x-FLI)
- Negative USDC amounts (representing borrowed positions)
- Complex derivative products
- Investment strategy tokens

### unauthorized.json
Error response for unauthorized API access:
- HTTP 401 status code
- Error headers including CloudFront and Istio metadata
- Standard error response structure
- Used for testing authentication error handling

### unknown_chain_response.json
Test data with an invalid blockchain identifier:
- Contains "this-chain-will-never-exist" as chain value
- Tests error handling for unsupported chains
- Otherwise valid portfolio structure

### usage_response.json
API usage statistics response showing:
- Current balance and daily usage stats
- Historical usage data over 30 days
- Remaining API calls per day
- Used for testing rate limit monitoring

## Integration Points

These test files integrate with:
- DeBank API client parsers that convert JSON responses to internal data models
- Error handling mechanisms for API failures
- Chain/protocol mapping logic
- Token price and metadata enrichment
- Portfolio aggregation and calculation engines

## Testing Patterns

The test data covers:
1. **Success Cases**: Valid responses with various data structures
2. **Error Cases**: Authentication failures, unknown chains
3. **Edge Cases**: Negative amounts, vesting positions, complex derivatives
4. **Data Variations**: Different protocols, chains, and position types

## Important Conventions

- All amounts are provided in both human-readable and raw formats
- Timestamps are Unix timestamps (seconds since epoch)
- Token addresses are checksummed Ethereum addresses
- Chain identifiers follow DeBank's naming convention (eth, bsc, matic, etc.)
- Prices are in USD with high precision decimals