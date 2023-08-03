from typing import Optional

from eth_utils import to_checksum_address


def make_checksum_address(address: str) -> Optional[str]:
    try:
        return to_checksum_address(address)
    except ValueError as e:
        return None
