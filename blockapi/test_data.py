from os import environ

test_addresses = {
    'BTC': [
        '35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP',
        'xpub6CUGRUonZSQ4TWtTMmzXdrXDtypWKiKrhko4egpiMZbpiaQL2jkwSB1icqYh2cfDfVxdx4df189oLKnC5fSwqPfgyP3hooxujYzAu3fDVmz',
        # 'ypub6WjHjrJLKSg8oQw1E4LGvQDJ2uofgMfJKLnv5Ha4NPRW4rf7LPXffMJ8EReixY1mUCc33SsiDUodUCTvCktFeN7ZW28GVhBXhNnoKYUqXbP',
    ],
    'BCH': [
        '35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP',
    ],
    'BSV': ['1M4CZGNmAv3o33wYoMLATJp4y4BTDe2okd'],
    'ADA': [
        'DdzFFzCqrhtCYb5skdVUvyKJ7AohbUesTsTB4GQbfqRmXU4X7Y2v6YwQCjANWcF3Add7yVn3JqtAC2n2jPZymEX5k7w2gFFnsaWpfZkW'
    ],
    'EOS': ['fzrv13xeykgc'],
    'ETH': ['0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca'],
    'LTC': ['M8T1B2Z97gVdvmfkQcAtYbEepune1tzGua'],
    'XTZ': [
        'tz1bDXD6nNSrebqmAnnKKwnX1QdePSMCj4MX',
        'KT1CRN88fn8EdWmZT9954Xf8NDsGfxtuwome',
    ],
    'DCR': [
        'DsjshD6PK3rgcKZtNUP7jnMcGQRvbY3dmwo',
        'DcrP3rA8RSi8Ai9VZU2pB2m31c9GWhEqii8',
        # current api doesn't support xpub key
        # 'dpubZFwoKEEJYVDxGo8bf2E4qwh6Qve9cku5gvaS5kC96hUdMT7SF9nymaLFeEFQaHy8a3SuiUJRL87rz3bfwFSFqErYVeHUg3xnzPjHftiofFu',
    ],
    'ATOM': ['cosmos1gn326f6sza44xt5kxrsdrnapp2sxhav03rhcsz'],
    'NEO': ['AZnTM3mYbx9yzg8tb6hr7w9pAKntDmrtqk'],
    'DOGE': ['DH5yaieqoZN36fDVciNyRueRGvGLR3mr7L'],
    'ZEC': ['t1VShHAhsQc5RVndQLyM1ZbQXLHKd35GkG1'],
    'DASH': ['XtAG1982HcYJVibHxRZrBmdzL5YTzj4cA1'],
    'ETC': ['0x618F37D7ff7B140E604172466CD42D1Ec35E0544'],
    'ZEN': ['znZTLu1asaLWxB7EBqBRQ6DCnNyctYA3Rm4'],
    'BNB': ['bnb1jxfh2g85q3v0tdq56fnevx6xcxtcnhtsmcu64m'],
    'XLM': ['GDD7ABRF7BCK76W33RXDQG5Q3WXVSQYVLGEMXSOWRGZ6Z3G3M2EM2TCP'],
    'RVN': ['RK6wMGc1tvLNDf4LoW6uoEcdUJVRfKsC7h'],
    'TRX': ['TNNc1HGDUrRkowQxdcUaWyBodZXshuVtBp'],
    'GRS': ['Fr5m2irs9vNWSAFXJK6KPtxqW9YWg384FX'],
    'VET': ['0xcE6b1252b32a34fc4013F096cDf90643fB5D23ba'],
    'BOS': ['GCPQQIX2LRX2J63C7AHWDXEMNGMZR2UI2PRN5TCSOVMEMF7BAUADMKH5'],
    'LUNA': ['terra1vw96exejy03w7n2jt8t3qv392f3lqtvmv53720'],
    'SOL': ['31dpiondDhZaqK23Re8kzkhY6CFEG9ZTQnr3shQm7g8b'],
    'ONT': ['AS5R2tAn2KViJN3W4KkW5XwrrR85sXpn9p'],
    'STAKE': ['0x6a1cf24C645DB2e37141Fa12E70Cb67e56b336f3'],
    'DOT': ['13vrWSUXdm9yJH4GPig2NDMJFxUHwepeUbHgBr6Kmya9eVLh'],
    'WND': ['5GeeixzC3xcCGc4Usi2UnCTfh46WXBmVL1duL9Nx5NHJkGxs'],
}


def get_test_api_key(api_cls_name):
    """Tries to load api key from environment."""
    if api_cls_name.startswith('CryptoID'):
        key_field = 'CRYPTOIDAPI_KEY'
    else:
        key_field = f'{api_cls_name.upper()}_KEY'

    return environ.get(key_field)
