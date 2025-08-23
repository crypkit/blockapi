# blockapi/utils Directory Structure

## Overview

This directory contains utility functions that provide common functionality for the blockapi library. These utilities handle various aspects of blockchain-related data processing including address validation, datetime parsing, numerical conversions (especially for blockchain decimals/raw values), and HTTP request user agent management.

## Files

### `__init__.py`
- **Purpose**: Package initialization file (currently empty)
- **Functionality**: Makes the utils directory a Python package

### `address.py`
- **Purpose**: Ethereum address validation and formatting utilities
- **Key Functions**:
  - `make_checksum_address(address: str) -> Optional[str]`: Converts an Ethereum address to its checksum format using eth_utils
  - Returns None if the address is invalid instead of raising an exception
- **Dependencies**: `eth_utils`
- **Usage**: Essential for validating and normalizing Ethereum addresses before blockchain interactions

### `datetime.py`
- **Purpose**: DateTime parsing utilities for blockchain timestamps
- **Key Functions**:
  - `parse_dt(dt: Union[str, int, float]) -> datetime`: Universal datetime parser that handles multiple input formats
    - String timestamps (e.g., "1234567890")
    - Integer/float timestamps
    - ISO format strings and other date formats via dateutil
- **Dependencies**: `dateutil`
- **Usage**: Standardizes datetime handling across different blockchain APIs that return timestamps in various formats

### `num.py`
- **Purpose**: Numerical conversion utilities optimized for blockchain decimal/raw value conversions
- **Key Functions**:
  - `to_int(number: Union[int, str])`: Safe integer conversion
  - `to_decimal(number: Union[int, float, str, Decimal]) -> Decimal`: Converts various number types to Decimal (handles float precision issues)
  - `raw_to_decimals(raw: Union[int, str], decimals: Union[int, str]) -> Decimal`: Converts raw blockchain values (wei, gwei, satoshi) to decimal format
  - `decimals_to_raw(amount: Union[int, str], decimals: Union[int, str]) -> Decimal`: Converts decimal values back to raw format
  - `remove_exponent(d: Decimal) -> Decimal`: Removes scientific notation from Decimal values
  - `safe_opt_decimal(obj: Optional[SupportsNumber]) -> Decimal`: Safely converts optional numbers to Decimal (None becomes 0)
  - `safe_decimal(number: SupportsNumber) -> Decimal`: Duplicate of to_decimal function
- **Key Patterns**: Heavy use of Decimal for precision, essential for handling cryptocurrency values
- **Usage**: Critical for accurate cryptocurrency amount calculations and conversions between different decimal precisions

### `user_agent.py`
- **Purpose**: HTTP user agent generation for API requests
- **Key Functions**:
  - `get_random_user_agent() -> str`: Returns a random user agent string
- **Dependencies**: `fake_useragent`
- **Usage**: Helps avoid rate limiting and blocking when making requests to blockchain APIs and explorers

## Architecture Patterns

1. **Error Handling**: The utilities favor returning None or default values rather than raising exceptions (e.g., `make_checksum_address`)
2. **Type Safety**: Extensive use of type hints with Union types to handle multiple input formats
3. **Precision Focus**: Heavy emphasis on Decimal type for numerical operations to avoid floating-point precision issues critical in financial calculations
4. **Timezone Awareness**: All datetime operations use UTC timezone to maintain consistency across different blockchain networks

## Integration Points

- These utilities are likely used throughout the blockapi library for:
  - Validating user-provided addresses before API calls
  - Parsing timestamps from various blockchain explorers
  - Converting between different token decimal formats (e.g., ETH has 18 decimals)
  - Setting appropriate headers for HTTP requests to blockchain APIs

## Important Conventions

- All numerical operations involving cryptocurrency amounts use Decimal type
- Datetime operations always use UTC timezone
- Invalid inputs typically return None rather than raising exceptions (defensive programming)