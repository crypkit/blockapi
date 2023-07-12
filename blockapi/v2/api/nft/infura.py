from typing import Optional

from pydantic import BaseModel

from blockapi.v2.base import ApiException, BlockchainApi, INftParser, INftProvider
from blockapi.v2.models import (
    ApiOptions,
    AssetType,
    Blockchain,
    Coin,
    CoinInfo,
    NftBalanceItem,
)


class InfuraNftAssetAttribute(BaseModel):
    key: str
    trait_type: str
    value: str


class InfuraNftAssetMetadata(BaseModel):
    name: str
    description: str
    image: str
    external_url: str
    token_id: int
    attributes: list[InfuraNftAssetAttribute]


class InfuraNftAsset(BaseModel):
    contract: str
    tokenId: str
    supply: str
    type: str
    metadata: InfuraNftAssetMetadata


class InfuraNftAssetsResponse(BaseModel):
    total: int
    pageNumber: int
    pageSize: int
    network: str
    account: str
    cursor: Optional[str]
    assets: list[InfuraNftAsset]


class InfuraNftApi(BlockchainApi, INftProvider, INftParser):
    """
    Infura NFT API
    Doc: https://docs.api.infura.io/nft/
    """

    def __init__(self, api_key: str):
        super().__init__(api_key)

    api_options = ApiOptions(
        blockchain=Blockchain.ETHEREUM,
        base_url='https://nft.api.infura.io/networks/',
        rate_limit=0.1,
    )

    chain_id = 1

    coin = None

    supported_requests = {'fetch_nft': '{chain_id}/accounts/{address}/assets/nfts'}

    def fetch_nft(self, address: str) -> dict:
        items = []
        cursor = None
        try:
            while True:
                response = self._fetch_single_page(address, cursor)
                items.append(InfuraNftAssetsResponse(**response))
                cursor = response.get('cursor')
                if not cursor:
                    break

        except ApiException as e:
            return dict(items=items, error=str(e))

        return dict(items=items)

    def parse_nft(self, data: dict) -> dict:
        balances = list(self._parse_items(data['items']))
        return dict(balances=balances)

    def _fetch_single_page(self, address, cursor):
        params = dict(cursor=cursor) if cursor else None
        response = self.get(
            'fetch_nft',
            headers=dict(
                accept='application/json', authorization=f'Basic {self.api_key}'
            ),
            params=params,
            chain_id=self.chain_id,
            address=address,
        )

        return response

    def _parse_items(self, items):
        for item in items:
            yield from self._parse_assets(item)

    @staticmethod
    def _parse_assets(item):
        re = InfuraNftAssetsResponse(**item)
        for asset in re.assets:
            coin = Coin.from_api(
                blockchain=Blockchain.ETHEREUM,
                decimals=0,
                symbol=str(asset.metadata.token_id),
                info=CoinInfo.from_api(
                    website=asset.metadata.external_url, logo_url=asset.metadata.image
                ),
            )

            yield NftBalanceItem.nft_from_api(
                balance_raw=int(asset.supply),
                coin=coin,
                name=asset.metadata.name,
                description=asset.metadata.description,
                asset_type=AssetType.AVAILABLE,
                raw=asset.dict(),
            )
