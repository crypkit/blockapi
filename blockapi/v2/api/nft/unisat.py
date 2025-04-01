import logging
from typing import Optional

from blockapi.v2.base import BlockchainApi, INftParser, INftProvider
from blockapi.v2.coins import COIN_BTC
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    Blockchain,
    Coin,
    ContractInfo,
    FetchResult,
    NftToken,
    ParseResult,
)

logger = logging.getLogger(__name__)


class UnisatApi(BlockchainApi, INftParser, INftProvider):
    """
    Bitcoin Ordinals
    API docs: https://docs.unisat.io/
    
    This API requires an API key from Unisat. You can get one by:
    1. Going to https://developer.unisat.io/account/login
    2. Creating an account
    3. Going to the API section
    4. Generating an API key
    """

    coin = COIN_BTC

    api_options = ApiOptions(
        blockchain=Blockchain.BITCOIN,
        base_url='https://open-api.unisat.io/v1/indexer',
        rate_limit=0.2,  # 5 calls per second for free tier
    )

    supported_requests = {
        'get_nfts': '/address/{address}/inscription-data',
    }

    def __init__(self, api_key: str):
        """
        Initialize the Unisat API client
        
        Args:
            api_key: Your Unisat API key. Required for all API calls.
        """
        if not api_key:
            raise ValueError("API key is required for Unisat API")
            
        super().__init__()
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def fetch_nfts(self, address: str, cursor: Optional[int] = None, size: int = 16) -> FetchResult:
        """
        Fetch NFTs (inscriptions) owned by the address
        
        Args:
            address: BTC address to fetch NFTs for
            cursor: Pagination cursor (offset)
            size: Number of items to return per page (default: 16)
            
        Returns:
            FetchResult containing the NFT data
            
        Raises:
            ValueError: If address is empty or invalid
        """
        if not address:
            raise ValueError("Address is required")
            
        params = {'size': size}
        if cursor is not None:
            params['cursor'] = cursor

        try:
            return self.get_data(
                'get_nfts',
                headers=self.headers,
                params=params,
                address=address,
                extra=dict(address=address),
            )
        except Exception as e:
            logger.error(f"Error fetching NFTs for address {address}: {str(e)}")
            return FetchResult(errors=[str(e)])

    def parse_nfts(self, fetch_result: FetchResult) -> ParseResult:
        """
        Parse NFT data from the API response
        
        Args:
            fetch_result: Raw API response data
            
        Returns:
            ParseResult containing parsed NFT tokens
        """
        if not fetch_result or not fetch_result.data:
            return ParseResult(errors=fetch_result.errors if fetch_result else None)

        try:
            parsed = list(self._yield_parsed_nfts(fetch_result.data))
            return ParseResult(
                data=parsed,
                errors=fetch_result.errors,
                cursor=fetch_result.data.get('cursor'),
            )
        except Exception as e:
            logger.error(f"Error parsing NFT data: {str(e)}")
            return ParseResult(errors=[str(e)])

    def _yield_parsed_nfts(self, data: dict):
        """
        Yield parsed NFT tokens from the API response
        
        Args:
            data: API response data containing inscription list
        """
        inscriptions = data.get('inscription', [])
        if not inscriptions:
            return

        for inscription in inscriptions:
            try:
                # Get required fields from the actual API response
                inscription_id = inscription.get('inscriptionId')
                inscription_number = inscription.get('inscriptionNumber')
                utxo = inscription.get('utxo', {})
                txid = utxo.get('txid')
                
                # Check required fields that must be present
                if not all([inscription_id, inscription_number, txid]):
                    logger.warning(
                        f"Skipping inscription with missing required fields. "
                        f"inscription_id: {inscription_id}, "
                        f"inscription_number: {inscription_number}, "
                        f"txid: {txid}"
                    )
                    continue

                # Create NFT token with only the fields we actually have
                yield NftToken.from_api(
                    ident=inscription_id,
                    collection='ordinals',
                    collection_name='Bitcoin Ordinals',
                    contract=txid,
                    standard='ordinals',
                    name=f"Ordinal #{inscription_number}",  # Using inscription number as name
                    description=None,  # Not in API response
                    amount=1,
                    image_url='',  # Required but not in API response
                    metadata_url=None,  # Not in API response
                    updated_time=inscription.get('timestamp'),
                    is_disabled=False,
                    is_nsfw=False,
                    blockchain=Blockchain.BITCOIN,
                    asset_type=AssetType.AVAILABLE,
                    market_url=None,  # Not in API response
                )
            except Exception as e:
                logger.error(f"Error parsing inscription {inscription.get('inscriptionId', 'unknown')}: {str(e)}")
                continue 