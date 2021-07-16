# blockapi

Library to interact with numerous cryptocurrency data APIs to get the basic info about account balance, transactions, staking informations, etc.
List of supported coins:

| coin  | API name | supported operations
| :---- | :------------| :---------------------
| XTZ   | TzscanAPI   | balance, transactions, activations, originations, delegations, endorsements, bakings
|       | TzStatsAPI  | staking (balance, rewards)
| ATOM  | CosmosAPI   | balance, transactions, rewards, delegates, votes
| DCR   | DcrdataAPI  | balance, transactions
| ADA   | CardanoExplorerAPI | balance, transactions
| ZEC   | ChainSoAPI  | balance, transactions
|       | MercerweissAPI | balance
|       | ZchainAPI | balance
| ETC   | BlockscoutAPI | balance
| NEO   | NeoscanAPI | balance, transactions
| ZEN   | ZensystemAPI | balance
| DASH  | ChainSoAPI | balance, transactions
|       | CryptoIDAPI | balance
| DOGE  | ChainSoAPI |balance, transactions
| BNB   | BinanceAPI |balance,transactions
| EOS   | EosparkAPI |balance, transactions
|       | GreymassAPI | balance
| BCH   | BtcAPI | balance
| XLM   | StellarAPI | balance
| RVN   | RavencoinAPI | balance
| TRX   | TronscanAPI | balance
| LTC   | BlockcypherAPI | balance
|       | ChainSoAPI | balance, transactions
|       | CryptoIDAPI | balance
|       | Ltc1TrezorAPI | balance, transactions
| BTC   | BlockchainInfoAPI | balance, transactions
|       | BlockonomicsAPI | balance, transactions
|       | ChainSoAPI | balance, transactions
|       | Btc1TrezorAPI | balance, transactions
|       | Btc2TrezorAPI | balance, transactions
|       | BitpayAPI | balance
| GRS   | CryptoIDAPI | balance
| ETH   | AlethioAPI | balance, transactions, events 
|       | EtherscanAPI | balance, transactions
|       | EthplorerAPI | balance
| ONT   | OntioAPI | balance, transactions
| VET   | DigonchainAPI | balance
| BOS   | BlockchainosAPI | balance, transactions
| LUNA  | TerraMoneyAPI | balance, transactions, delegations
| DOT   | SubscanPolkaAPI | balance, transactions, staking (locked, rewards)
| KSM   | SubscanKusamaAPI | balance, transactions, staking (locked, rewards)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python 3.x, PIP (if you'd like to install it this way).

### Installing

Library can be installed simply with pip:

```
pip install blockapi
```

or by running:
```
make install
```

### Usage examples

Example usage to get account balance:
```
import blockapi
myobj = blockapi.api.BlockchainInfoAPI("bitcoin-address-here")
myobj.get_balance()
```

For some coins there are multiple APIs available. With get_random_api_class_for_coin it is possible
to randomly pick any of the available APIs:
```
myapi = blockapi.get_random_api_class_for_coin('BTC')('1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX')
myapi.get_balance()
```

To directly pick first random working API and ask it for the account balance:
```
>>> blockapi.get_balance_from_random_api('BTC','16ftSEQ4ctQFDtVZiUBusQUjRrGhM3JYwe')
0.010034040000000001
```

It is possible to ask for a list of working APIs for a coin. They are automatically checked first if they work (test is done with asking for a balance). Only APIs which pass this check are returned:
```
>>> blockapi.get_working_apis_for_coin('BTC')
(<class 'blockapi.api.blockchaininfo.BlockchainInfoAPI'>, <class 'blockapi.api.blockonomics.BlockonomicsAPI'>, <class 'blockapi.api.insight.BitpayAPI'>, <class 'blockapi.api.trezor.Btc2TrezorAPI'>, <class 'blockapi.api.trezor.Btc1TrezorAPI'>)
```

During the API instance creation the supplied address is being checked for validity, if the address
is not valid, ValueError exception is being raised:
```
>>> import blockapi
>>> blockapi.api.CosmosAPI('blahblah')
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "/srv/apps/blockapi/src/blockapi/blockapi/services.py", line 195, in __init__
self.check_validity()
File "/srv/apps/blockapi/src/blockapi/blockapi/services.py", line 201, in check_validity
self.symbol, self.address_info.address
ValueError: Not a valid ATOM address: b'blahblah'
```

It is possible to display the result of the address validation with included details like validity, network type, address type, or the info whether the supplied address is an extended one.
Not for all coins all the details are available though:
```
>>> import blockapi
>>> myapi = blockapi.api.TzscanAPI('valid tezos address here')
>>> myapi.address_info
ValidationResult(name='tezos', ticker='xtz', address=b'valid tezos-address here', valid=True, network='both', is_extended=False, address_type='originated_account')
```

## Running the tests

To run the included tests simply issue:

```
make test
```

## Contributing

TBD

## Authors

* **Devmons s.r.o. - *Initial work* - [crypkit](https://github.com/crypkit)

See also the list of [contributors](https://github.com/crypkit/blockapi/contributors) who participated in this project.

## Credits

* **Chris Priest - *moneywagon library we took many ideas from* - [moneywagon](https://github.com/priestc/moneywagon)
* **Joe Black - *Address validation library* - [coinaddr](https://github.com/joeblackwaslike/coinaddr)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

