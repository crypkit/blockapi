# Test Data Directory Structure

## Overview
This directory contains mock response data files used for testing the blockapi v2 API integration. The data represents real-world API responses from various blockchain explorers, NFT marketplaces, and cryptocurrency data providers. These files serve as test fixtures for unit and integration tests, ensuring the blockapi library correctly parses and handles responses from different blockchain data sources.

## Directory Contents

### Bitcoin and Bitcoin-like Blockchain Data

#### Blockchair Response Files
- **blockchair_btc_balance_response.json**: Bitcoin address balance and transaction data from Blockchair API. Contains detailed address information including balance, transaction history, and UTXO data.
- **blockchair_btc_transaction_response.json**: Bitcoin transaction details from Blockchair API.
- **blockchair_doge_balance_response.json**: Dogecoin address balance response in Blockchair format.
- **blockchair_doge_transaction_response.json**: Dogecoin transaction details from Blockchair.
- **blockchair_ltc_balance_response.json**: Litecoin address balance response.
- **blockchair_ltc_transaction_response.json**: Litecoin transaction details.

#### Trezor/Blockbook Response Files
- **trezor_btc_1_balance_response.json**: Bitcoin balance data from Trezor's Blockbook API (first test case).
- **trezor_btc_2_balance_response.json**: Bitcoin balance data from Trezor's Blockbook API (second test case).
- **trezor_xpub_1_balance_response.json**: Extended public key (xpub) balance data showing hierarchical deterministic wallet information.
- **trezor_xpub_2_balance_response.json**: Second xpub test case with different wallet structure.

### Ethereum and EVM-Compatible Chain Data

- **ethplorer_balance_response.json**: Ethereum address balance including ETH and ERC-20 token holdings. Shows detailed token information with prices, decimals, and market data.
- **optimistic_etherscan_balance_response.json**: Optimism network balance data in Etherscan-compatible format.

### Blockchain Operating System (BOS) Data

- **bos_balance_response.json**: BOS blockchain balance information.
- **bos_transaction_response.json**: BOS transaction details.
- **bos_operations_response_8t_1.json**: BOS operations data for transaction starting with "8t" (part 1).
- **bos_operations_response_8t_2.json**: BOS operations data for transaction starting with "8t" (part 2).
- **bos_operations_response_r1_1.json**: BOS operations data for transaction starting with "r1" (part 1).
- **bos_operations_response_r1_2.json**: BOS operations data for transaction starting with "r1" (part 2).

### Polkadot/Substrate Chain Data

- **subscan_polkadot_response_DCK.json**: Polkadot account data from Subscan API for address ending in "DCK". Contains balance, locks, staking, and proxy information.
- **subscan_polkadot_response_WE9.json**: Polkadot account data for address ending in "WE9".

### Subdirectories

#### magiceden/
NFT marketplace data from Magic Eden (primarily Solana and Bitcoin Ordinals):
- **collection-stats.json**: Collection statistics including floor price, volume, and listed count.
- **listings.json**: Active NFT listings data.
- **offers.json**: Collection offers data.
- **wallet-response.json**: Wallet NFT holdings response.

#### opensea/
NFT marketplace data from OpenSea:
- **collection-stats.json**: Detailed collection statistics with volume intervals (daily, weekly, monthly).
- **collection.json**: Collection metadata and configuration.
- **listings-locked.json**: Locked/restricted NFT listings.
- **listings.json**: Standard NFT listings.
- **nfts-next.json**: Paginated NFT data (next page).
- **nfts.json**: NFT holdings and metadata.
- **offers-next.json**: Paginated offers data.
- **offers.json**: Collection and item offers.

#### simplehash/
Multi-chain NFT data aggregator responses:
- **collection-activity.json**: Collection trading activity and events.
- **collection.json**: Collection metadata including floor prices from multiple marketplaces.
- **fungibles.json**: Fungible token (ERC-20/SPL) holdings.
- **listings.json**: Cross-marketplace NFT listings.
- **nfts.json**: NFT ownership and metadata.
- **offers.json**: Aggregated offers data.
- **solana-listings-nfts.json**: Solana-specific NFT listings.
- **solana-nfts.json**: Solana NFT holdings.

#### solana/
Solana blockchain and ecosystem data:
- **ban-list-jup-ag.csv**: Jupiter aggregator's banned token list with scam/fake tokens.
- **rent_reserve_solana_response.json**: Solana rent reserve calculation data.
- **solana_response.json**: General Solana account/balance data.
- **staked_solana_response.json**: Staked SOL information.
- **token-list-jup-ag.csv**: Jupiter aggregator's supported token list with metadata.
- **token-list-solana.json**: Solana token registry in JSON format.
- **token-list-sonar.json**: Alternative Solana token list from Sonar.

#### sui/
Sui blockchain data:
- **response.json**: Sui wallet balance response showing multiple coin types with USD values.

#### unisat/
Bitcoin Ordinals marketplace (Unisat) data:
- **collection_info.json**: Basic collection information (holders, items, block height).
- **collection_items.json**: Individual inscription items in a collection.
- **collection_stats.json**: Collection trading statistics.
- **collection_stats_full_url.json**: Stats response with complete URL formatting.
- **collection_stats_v4.json**: Version 4 API stats response.
- **inscription_data.json**: Individual inscription metadata.
- **inscription_data_edge_cases.json**: Edge case inscription data for testing.
- **listings.json**: Ordinals marketplace listings.
- **offers.json**: Collection offers on Unisat.

## Usage Patterns

These test data files are used to:
1. **Mock API Responses**: Provide realistic data for unit tests without making actual API calls.
2. **Test Parser Logic**: Ensure response parsing handles various data formats and edge cases.
3. **Integration Testing**: Validate that the blockapi library correctly processes responses from different blockchain data providers.
4. **Edge Case Testing**: Files like `inscription_data_edge_cases.json` specifically test handling of unusual or problematic data.

## Key Observations

- **Multi-chain Support**: Data covers Bitcoin, Ethereum, Solana, Polkadot, Sui, and other blockchains.
- **NFT Focus**: Significant emphasis on NFT marketplace data from multiple providers (OpenSea, Magic Eden, SimpleHash, Unisat).
- **Standardized Formats**: Many responses follow similar patterns (balance, transactions, listings) adapted for each blockchain.
- **Real-world Data**: Files contain actual API response structures, ensuring tests reflect production scenarios.