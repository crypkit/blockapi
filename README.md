# blockapi

Library to interact with numerous cryptocurrency data APIs to get the basic info about account balance, transactions, ...

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

Example usage to get account balance:
```
import blockapi.api
from blockapi.api.blockchaininfo import BlockchainInfoAPI
myobj = BlockchainInfoAPI("bitcoin-address-here")
myobj.get_balance()
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

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

