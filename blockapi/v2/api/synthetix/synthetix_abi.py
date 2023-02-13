synthetix_abi = [
    {
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_proxy",
                "type": "address",
            },
            {
                "internalType": "contract TokenState",
                "name": "_tokenState",
                "type": "address",
            },
            {"internalType": "address", "name": "_owner", "type": "address"},
            {
                "internalType": "uint256",
                "name": "_totalSupply",
                "type": "uint256",
            },
            {
                "internalType": "address",
                "name": "_resolver",
                "type": "address",
            },
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "snxRedeemed",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amountLiquidated",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "liquidator",
                "type": "address",
            },
        ],
        "name": "AccountLiquidated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256",
            },
        ],
        "name": "ExchangeRebate",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256",
            },
        ],
        "name": "ExchangeReclaim",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "trackingCode",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "toCurrencyKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "toAmount",
                "type": "uint256",
            },
        ],
        "name": "ExchangeTracking",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldOwner",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnerChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            }
        ],
        "name": "OwnerNominated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "proxyAddress",
                "type": "address",
            }
        ],
        "name": "ProxyUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newBeneficiary",
                "type": "address",
            }
        ],
        "name": "SelfDestructBeneficiaryUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "selfDestructDelay",
                "type": "uint256",
            }
        ],
        "name": "SelfDestructInitiated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [],
        "name": "SelfDestructTerminated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "beneficiary",
                "type": "address",
            }
        ],
        "name": "SelfDestructed",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "fromCurrencyKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "fromAmount",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "toCurrencyKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "toAmount",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "toAddress",
                "type": "address",
            },
        ],
        "name": "SynthExchange",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newTokenState",
                "type": "address",
            }
        ],
        "name": "TokenStateUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "DECIMALS",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_ADDRESSES_FROM_RESOLVER",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "SELFDESTRUCT_DELAY",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "TOKEN_NAME",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "TOKEN_SYMBOL",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "acceptOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "anySynthOrSNXRateIsInvalid",
        "outputs": [{"internalType": "bool", "name": "anyRateInvalid", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "availableCurrencyKeys",
        "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "availableSynthCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "availableSynths",
        "outputs": [{"internalType": "contract ISynth", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "burnSynths",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "burnForAddress",
                "type": "address",
            },
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "burnSynthsOnBehalf",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "burnSynthsToTarget",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "burnForAddress",
                "type": "address",
            }
        ],
        "name": "burnSynthsToTargetOnBehalf",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "collateral",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "_issuer", "type": "address"}],
        "name": "collateralisationRatio",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
        ],
        "name": "debtBalanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "emitExchangeRebate",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "emitExchangeReclaim",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "trackingCode",
                "type": "bytes32",
            },
            {
                "internalType": "bytes32",
                "name": "toCurrencyKey",
                "type": "bytes32",
            },
            {"internalType": "uint256", "name": "toAmount", "type": "uint256"},
        ],
        "name": "emitExchangeTracking",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {
                "internalType": "bytes32",
                "name": "fromCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "fromAmount",
                "type": "uint256",
            },
            {
                "internalType": "bytes32",
                "name": "toCurrencyKey",
                "type": "bytes32",
            },
            {"internalType": "uint256", "name": "toAmount", "type": "uint256"},
            {
                "internalType": "address",
                "name": "toAddress",
                "type": "address",
            },
        ],
        "name": "emitSynthExchange",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "sourceCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "sourceAmount",
                "type": "uint256",
            },
            {
                "internalType": "bytes32",
                "name": "destinationCurrencyKey",
                "type": "bytes32",
            },
        ],
        "name": "exchange",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountReceived",
                "type": "uint256",
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "exchangeForAddress",
                "type": "address",
            },
            {
                "internalType": "bytes32",
                "name": "sourceCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "sourceAmount",
                "type": "uint256",
            },
            {
                "internalType": "bytes32",
                "name": "destinationCurrencyKey",
                "type": "bytes32",
            },
        ],
        "name": "exchangeOnBehalf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountReceived",
                "type": "uint256",
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "exchangeForAddress",
                "type": "address",
            },
            {
                "internalType": "bytes32",
                "name": "sourceCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "sourceAmount",
                "type": "uint256",
            },
            {
                "internalType": "bytes32",
                "name": "destinationCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "address",
                "name": "originator",
                "type": "address",
            },
            {
                "internalType": "bytes32",
                "name": "trackingCode",
                "type": "bytes32",
            },
        ],
        "name": "exchangeOnBehalfWithTracking",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountReceived",
                "type": "uint256",
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "sourceCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "sourceAmount",
                "type": "uint256",
            },
            {
                "internalType": "bytes32",
                "name": "destinationCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "address",
                "name": "originator",
                "type": "address",
            },
            {
                "internalType": "bytes32",
                "name": "trackingCode",
                "type": "bytes32",
            },
        ],
        "name": "exchangeWithTracking",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountReceived",
                "type": "uint256",
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "getResolverAddressesRequired",
        "outputs": [
            {
                "internalType": "bytes32[24]",
                "name": "addressesRequired",
                "type": "bytes32[24]",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "initiateSelfDestruct",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "initiationTime",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "integrationProxy",
        "outputs": [{"internalType": "contract Proxy", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "_resolver",
                "type": "address",
            }
        ],
        "name": "isResolverCached",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "isWaitingPeriod",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "issueMaxSynths",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "issueForAddress",
                "type": "address",
            }
        ],
        "name": "issueMaxSynthsOnBehalf",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "issueSynths",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "issueForAddress",
                "type": "address",
            },
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "issueSynthsOnBehalf",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {
                "internalType": "uint256",
                "name": "susdAmount",
                "type": "uint256",
            },
        ],
        "name": "liquidateDelinquentAccount",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "maxIssuableSynths",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "maxIssuable",
                "type": "uint256",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "messageSender",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "mint",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "_owner", "type": "address"}],
        "name": "nominateNewOwner",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "nominatedOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "proxy",
        "outputs": [{"internalType": "contract Proxy", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "remainingIssuableSynths",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "maxIssuable",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "alreadyIssued",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "totalSystemDebt",
                "type": "uint256",
            },
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolver",
        "outputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "",
                "type": "address",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "resolverAddressesRequired",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "sUSD",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "selfDestruct",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "selfDestructBeneficiary",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "selfDestructInitiated",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_integrationProxy",
                "type": "address",
            }
        ],
        "name": "setIntegrationProxy",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "sender", "type": "address"}],
        "name": "setMessageSender",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_proxy",
                "type": "address",
            }
        ],
        "name": "setProxy",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "_resolver",
                "type": "address",
            }
        ],
        "name": "setResolverAndSyncCache",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_beneficiary",
                "type": "address",
            }
        ],
        "name": "setSelfDestructBeneficiary",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "contract TokenState",
                "name": "_tokenState",
                "type": "address",
            }
        ],
        "name": "setTokenState",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "settle",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "reclaimed",
                "type": "uint256",
            },
            {"internalType": "uint256", "name": "refunded", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "numEntriesSettled",
                "type": "uint256",
            },
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "synths",
        "outputs": [{"internalType": "contract ISynth", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "address",
                "name": "synthAddress",
                "type": "address",
            }
        ],
        "name": "synthsByAddress",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "terminateSelfDestruct",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "tokenState",
        "outputs": [
            {
                "internalType": "contract TokenState",
                "name": "",
                "type": "address",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "totalIssuedSynths",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "totalIssuedSynthsExcludeEtherCollateral",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "transferableSynthetix",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "transferable",
                "type": "uint256",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

feepool_abi = [
    {
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_proxy",
                "type": "address",
            },
            {"internalType": "address", "name": "_owner", "type": "address"},
            {
                "internalType": "address",
                "name": "_resolver",
                "type": "address",
            },
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "feePeriodId",
                "type": "uint256",
            }
        ],
        "name": "FeePeriodClosed",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "sUSDAmount",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "snxRewards",
                "type": "uint256",
            },
        ],
        "name": "FeesClaimed",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "debtRatio",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "debtEntryIndex",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "feePeriodStartingDebtIndex",
                "type": "uint256",
            },
        ],
        "name": "IssuanceDebtRatioEntry",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldOwner",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnerChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            }
        ],
        "name": "OwnerNominated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "proxyAddress",
                "type": "address",
            }
        ],
        "name": "ProxyUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newBeneficiary",
                "type": "address",
            }
        ],
        "name": "SelfDestructBeneficiaryUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "selfDestructDelay",
                "type": "uint256",
            }
        ],
        "name": "SelfDestructInitiated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [],
        "name": "SelfDestructTerminated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "beneficiary",
                "type": "address",
            }
        ],
        "name": "SelfDestructed",
        "type": "event",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "FEE_ADDRESS",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "FEE_PERIOD_LENGTH",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_ADDRESSES_FROM_RESOLVER",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "SELFDESTRUCT_DELAY",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "acceptOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {
                "internalType": "uint256",
                "name": "debtRatio",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "debtEntryIndex",
                "type": "uint256",
            },
        ],
        "name": "appendAccountIssuanceRecord",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "quantity", "type": "uint256"},
        ],
        "name": "appendVestingEntry",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "claimFees",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "claimingForAddress",
                "type": "address",
            }
        ],
        "name": "claimOnBehalf",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "closeCurrentFeePeriod",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "period", "type": "uint256"},
        ],
        "name": "effectiveDebtRatioForPeriod",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "feePeriodDuration",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "feesAvailable",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "feesByPeriod",
        "outputs": [
            {
                "internalType": "uint256[2][2]",
                "name": "results",
                "type": "uint256[2][2]",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "address",
                "name": "_claimingAddress",
                "type": "address",
            }
        ],
        "name": "getLastFeeWithdrawal",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "getPenaltyThresholdRatio",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "getResolverAddressesRequired",
        "outputs": [
            {
                "internalType": "bytes32[24]",
                "name": "addressesRequired",
                "type": "bytes32[24]",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint256",
                "name": "feePeriodIndex",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "feePeriodId",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "startingDebtIndex",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "startTime",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "feesToDistribute",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "feesClaimed",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "rewardsToDistribute",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "rewardsClaimed",
                "type": "uint256",
            },
        ],
        "name": "importFeePeriod",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "initiateSelfDestruct",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "initiationTime",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "integrationProxy",
        "outputs": [{"internalType": "contract Proxy", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "isFeesClaimable",
        "outputs": [{"internalType": "bool", "name": "feesClaimable", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "_resolver",
                "type": "address",
            }
        ],
        "name": "isResolverCached",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "issuanceRatio",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "messageSender",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "_owner", "type": "address"}],
        "name": "nominateNewOwner",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "nominatedOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "proxy",
        "outputs": [{"internalType": "contract Proxy", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "recentFeePeriods",
        "outputs": [
            {
                "internalType": "uint64",
                "name": "feePeriodId",
                "type": "uint64",
            },
            {
                "internalType": "uint64",
                "name": "startingDebtIndex",
                "type": "uint64",
            },
            {"internalType": "uint64", "name": "startTime", "type": "uint64"},
            {
                "internalType": "uint256",
                "name": "feesToDistribute",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "feesClaimed",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "rewardsToDistribute",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "rewardsClaimed",
                "type": "uint256",
            },
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "recordFeePaid",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolver",
        "outputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "",
                "type": "address",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "resolverAddressesRequired",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "selfDestruct",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "selfDestructBeneficiary",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "selfDestructInitiated",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_integrationProxy",
                "type": "address",
            }
        ],
        "name": "setIntegrationProxy",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "sender", "type": "address"}],
        "name": "setMessageSender",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_proxy",
                "type": "address",
            }
        ],
        "name": "setProxy",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "_resolver",
                "type": "address",
            }
        ],
        "name": "setResolverAndSyncCache",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "setRewardsToDistribute",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_beneficiary",
                "type": "address",
            }
        ],
        "name": "setSelfDestructBeneficiary",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "setupExpiryTime",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "targetThreshold",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "terminateSelfDestruct",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalFeesAvailable",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalRewardsAvailable",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

exchangerates_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "_owner", "type": "address"},
            {"internalType": "address", "name": "_oracle", "type": "address"},
            {
                "internalType": "address",
                "name": "_resolver",
                "type": "address",
            },
            {
                "internalType": "bytes32[]",
                "name": "_currencyKeys",
                "type": "bytes32[]",
            },
            {
                "internalType": "uint256[]",
                "name": "_newRates",
                "type": "uint256[]",
            },
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "aggregator",
                "type": "address",
            },
        ],
        "name": "AggregatorAdded",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "aggregator",
                "type": "address",
            },
        ],
        "name": "AggregatorRemoved",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "entryPoint",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "upperLimit",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "lowerLimit",
                "type": "uint256",
            },
        ],
        "name": "InversePriceConfigured",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "rate",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "initiator",
                "type": "address",
            },
        ],
        "name": "InversePriceFrozen",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOracle",
                "type": "address",
            }
        ],
        "name": "OracleUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldOwner",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnerChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            }
        ],
        "name": "OwnerNominated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "RateDeleted",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32[]",
                "name": "currencyKeys",
                "type": "bytes32[]",
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "newRates",
                "type": "uint256[]",
            },
        ],
        "name": "RatesUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newBeneficiary",
                "type": "address",
            }
        ],
        "name": "SelfDestructBeneficiaryUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "selfDestructDelay",
                "type": "uint256",
            }
        ],
        "name": "SelfDestructInitiated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [],
        "name": "SelfDestructTerminated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "beneficiary",
                "type": "address",
            }
        ],
        "name": "SelfDestructed",
        "type": "event",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_ADDRESSES_FROM_RESOLVER",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "SELFDESTRUCT_DELAY",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "acceptOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "address",
                "name": "aggregatorAddress",
                "type": "address",
            },
        ],
        "name": "addAggregator",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "aggregatorKeys",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "aggregatorWarningFlags",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "aggregators",
        "outputs": [
            {
                "internalType": "contract AggregatorInterface",
                "name": "",
                "type": "address",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "currencyKeys",
                "type": "bytes32[]",
            }
        ],
        "name": "anyRateIsInvalid",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "canFreezeRate",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "address",
                "name": "aggregator",
                "type": "address",
            }
        ],
        "name": "currenciesUsingAggregator",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "currencies",
                "type": "bytes32[]",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "currentRoundForRate",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "deleteRate",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "sourceCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "sourceAmount",
                "type": "uint256",
            },
            {
                "internalType": "bytes32",
                "name": "destinationCurrencyKey",
                "type": "bytes32",
            },
        ],
        "name": "effectiveValue",
        "outputs": [{"internalType": "uint256", "name": "value", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "sourceCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "sourceAmount",
                "type": "uint256",
            },
            {
                "internalType": "bytes32",
                "name": "destinationCurrencyKey",
                "type": "bytes32",
            },
        ],
        "name": "effectiveValueAndRates",
        "outputs": [
            {"internalType": "uint256", "name": "value", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "sourceRate",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "destinationRate",
                "type": "uint256",
            },
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "sourceCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "sourceAmount",
                "type": "uint256",
            },
            {
                "internalType": "bytes32",
                "name": "destinationCurrencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "roundIdForSrc",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "roundIdForDest",
                "type": "uint256",
            },
        ],
        "name": "effectiveValueAtRound",
        "outputs": [{"internalType": "uint256", "name": "value", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "freezeRate",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "getCurrentRoundId",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "startingRoundId",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "startingTimestamp",
                "type": "uint256",
            },
            {"internalType": "uint256", "name": "timediff", "type": "uint256"},
        ],
        "name": "getLastRoundIdBeforeElapsedSecs",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "getResolverAddressesRequired",
        "outputs": [
            {
                "internalType": "bytes32[24]",
                "name": "addressesRequired",
                "type": "bytes32[24]",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "initiateSelfDestruct",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "initiationTime",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "inversePricing",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "entryPoint",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "upperLimit",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "lowerLimit",
                "type": "uint256",
            },
            {
                "internalType": "bool",
                "name": "frozenAtUpperLimit",
                "type": "bool",
            },
            {
                "internalType": "bool",
                "name": "frozenAtLowerLimit",
                "type": "bool",
            },
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "invertedKeys",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "_resolver",
                "type": "address",
            }
        ],
        "name": "isResolverCached",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "lastRateUpdateTimes",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "currencyKeys",
                "type": "bytes32[]",
            }
        ],
        "name": "lastRateUpdateTimesForCurrencies",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "_owner", "type": "address"}],
        "name": "nominateNewOwner",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "nominatedOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "oracle",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {"internalType": "uint256", "name": "roundId", "type": "uint256"},
        ],
        "name": "rateAndTimestampAtRound",
        "outputs": [
            {"internalType": "uint256", "name": "rate", "type": "uint256"},
            {"internalType": "uint256", "name": "time", "type": "uint256"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "rateAndUpdatedTime",
        "outputs": [
            {"internalType": "uint256", "name": "rate", "type": "uint256"},
            {"internalType": "uint256", "name": "time", "type": "uint256"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "rateForCurrency",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "rateIsFlagged",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "rateIsFrozen",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "rateIsInvalid",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "rateIsStale",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "rateStalePeriod",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "currencyKeys",
                "type": "bytes32[]",
            }
        ],
        "name": "ratesAndInvalidForCurrencies",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "rates",
                "type": "uint256[]",
            },
            {"internalType": "bool", "name": "anyRateInvalid", "type": "bool"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "numRounds",
                "type": "uint256",
            },
        ],
        "name": "ratesAndUpdatedTimeForCurrencyLastNRounds",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "rates",
                "type": "uint256[]",
            },
            {
                "internalType": "uint256[]",
                "name": "times",
                "type": "uint256[]",
            },
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "currencyKeys",
                "type": "bytes32[]",
            }
        ],
        "name": "ratesForCurrencies",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "removeAggregator",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "removeInversePricing",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolver",
        "outputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "",
                "type": "address",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "resolverAddressesRequired",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "selfDestruct",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "selfDestructBeneficiary",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "selfDestructInitiated",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "entryPoint",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "upperLimit",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "lowerLimit",
                "type": "uint256",
            },
            {
                "internalType": "bool",
                "name": "freezeAtUpperLimit",
                "type": "bool",
            },
            {
                "internalType": "bool",
                "name": "freezeAtLowerLimit",
                "type": "bool",
            },
        ],
        "name": "setInversePricing",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "_oracle", "type": "address"}],
        "name": "setOracle",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "_resolver",
                "type": "address",
            }
        ],
        "name": "setResolverAndSyncCache",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_beneficiary",
                "type": "address",
            }
        ],
        "name": "setSelfDestructBeneficiary",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "terminateSelfDestruct",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "currencyKeys",
                "type": "bytes32[]",
            },
            {
                "internalType": "uint256[]",
                "name": "newRates",
                "type": "uint256[]",
            },
            {"internalType": "uint256", "name": "timeSent", "type": "uint256"},
        ],
        "name": "updateRates",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

system_settings_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "_owner", "type": "address"},
            {
                "internalType": "address",
                "name": "_resolver",
                "type": "address",
            },
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "flags",
                "type": "address",
            }
        ],
        "name": "AggregatorWarningFlagsUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "name",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "destination",
                "type": "address",
            },
        ],
        "name": "CacheUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "enum MixinSystemSettings.CrossDomainMessageGasLimits",
                "name": "gasLimitType",
                "type": "uint8",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newLimit",
                "type": "uint256",
            },
        ],
        "name": "CrossDomainMessageGasLimitChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "debtSnapshotStaleTime",
                "type": "uint256",
            }
        ],
        "name": "DebtSnapshotStaleTimeUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "synthKey",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newExchangeFeeRate",
                "type": "uint256",
            },
        ],
        "name": "ExchangeFeeUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newFeePeriodDuration",
                "type": "uint256",
            }
        ],
        "name": "FeePeriodDurationUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newRatio",
                "type": "uint256",
            }
        ],
        "name": "IssuanceRatioUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newDelay",
                "type": "uint256",
            }
        ],
        "name": "LiquidationDelayUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newPenalty",
                "type": "uint256",
            }
        ],
        "name": "LiquidationPenaltyUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newRatio",
                "type": "uint256",
            }
        ],
        "name": "LiquidationRatioUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "minimumStakeTime",
                "type": "uint256",
            }
        ],
        "name": "MinimumStakeTimeUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldOwner",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnerChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            }
        ],
        "name": "OwnerNominated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "threshold",
                "type": "uint256",
            }
        ],
        "name": "PriceDeviationThresholdUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "rateStalePeriod",
                "type": "uint256",
            }
        ],
        "name": "RateStalePeriodUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newTargetThreshold",
                "type": "uint256",
            }
        ],
        "name": "TargetThresholdUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bool",
                "name": "enabled",
                "type": "bool",
            }
        ],
        "name": "TradingRewardsEnabled",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "waitingPeriodSecs",
                "type": "uint256",
            }
        ],
        "name": "WaitingPeriodSecsUpdated",
        "type": "event",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_CROSS_DOMAIN_GAS_LIMIT",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_EXCHANGE_FEE_RATE",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_FEE_PERIOD_DURATION",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_ISSUANCE_RATIO",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_LIQUIDATION_DELAY",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_LIQUIDATION_PENALTY",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_LIQUIDATION_RATIO",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_MINIMUM_STAKE_TIME",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_TARGET_THRESHOLD",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MIN_CROSS_DOMAIN_GAS_LIMIT",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MIN_FEE_PERIOD_DURATION",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MIN_LIQUIDATION_DELAY",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "RATIO_FROM_TARGET_BUFFER",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "acceptOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "aggregatorWarningFlags",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "enum MixinSystemSettings.CrossDomainMessageGasLimits",
                "name": "gasLimitType",
                "type": "uint8",
            }
        ],
        "name": "crossDomainMessageGasLimit",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "debtSnapshotStaleTime",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "currencyKey",
                "type": "bytes32",
            }
        ],
        "name": "exchangeFeeRate",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "feePeriodDuration",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "isResolverCached",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "issuanceRatio",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "liquidationDelay",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "liquidationPenalty",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "liquidationRatio",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "minimumStakeTime",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "_owner", "type": "address"}],
        "name": "nominateNewOwner",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "nominatedOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "priceDeviationThresholdFactor",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "rateStalePeriod",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "rebuildCache",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolver",
        "outputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "",
                "type": "address",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolverAddressesRequired",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "addresses",
                "type": "bytes32[]",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "_flags", "type": "address"}],
        "name": "setAggregatorWarningFlags",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "enum MixinSystemSettings.CrossDomainMessageGasLimits",
                "name": "_gasLimitType",
                "type": "uint8",
            },
            {
                "internalType": "uint256",
                "name": "_crossDomainMessageGasLimit",
                "type": "uint256",
            },
        ],
        "name": "setCrossDomainMessageGasLimit",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "_seconds", "type": "uint256"}],
        "name": "setDebtSnapshotStaleTime",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "synthKeys",
                "type": "bytes32[]",
            },
            {
                "internalType": "uint256[]",
                "name": "exchangeFeeRates",
                "type": "uint256[]",
            },
        ],
        "name": "setExchangeFeeRateForSynths",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_feePeriodDuration",
                "type": "uint256",
            }
        ],
        "name": "setFeePeriodDuration",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_issuanceRatio",
                "type": "uint256",
            }
        ],
        "name": "setIssuanceRatio",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "time", "type": "uint256"}],
        "name": "setLiquidationDelay",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "penalty", "type": "uint256"}],
        "name": "setLiquidationPenalty",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_liquidationRatio",
                "type": "uint256",
            }
        ],
        "name": "setLiquidationRatio",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "_seconds", "type": "uint256"}],
        "name": "setMinimumStakeTime",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_priceDeviationThresholdFactor",
                "type": "uint256",
            }
        ],
        "name": "setPriceDeviationThresholdFactor",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "period", "type": "uint256"}],
        "name": "setRateStalePeriod",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "_percent", "type": "uint256"}],
        "name": "setTargetThreshold",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bool",
                "name": "_tradingRewardsEnabled",
                "type": "bool",
            }
        ],
        "name": "setTradingRewardsEnabled",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_waitingPeriodSecs",
                "type": "uint256",
            }
        ],
        "name": "setWaitingPeriodSecs",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "targetThreshold",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "tradingRewardsEnabled",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "waitingPeriodSecs",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

erc20_abi = [
    {
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_proxy",
                "type": "address",
            },
            {
                "internalType": "contract TokenState",
                "name": "_tokenState",
                "type": "address",
            },
            {"internalType": "string", "name": "_tokenName", "type": "string"},
            {
                "internalType": "string",
                "name": "_tokenSymbol",
                "type": "string",
            },
            {"internalType": "address", "name": "_owner", "type": "address"},
            {
                "internalType": "bytes32",
                "name": "_currencyKey",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "_totalSupply",
                "type": "uint256",
            },
            {
                "internalType": "address",
                "name": "_resolver",
                "type": "address",
            },
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Burned",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "name",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "destination",
                "type": "address",
            },
        ],
        "name": "CacheUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Issued",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldOwner",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnerChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            }
        ],
        "name": "OwnerNominated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "proxyAddress",
                "type": "address",
            }
        ],
        "name": "ProxyUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newTokenState",
                "type": "address",
            }
        ],
        "name": "TokenStateUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "DECIMALS",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "FEE_ADDRESS",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "acceptOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "burn",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "currencyKey",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "integrationProxy",
        "outputs": [{"internalType": "contract Proxy", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "isResolverCached",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "issue",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "messageSender",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "_owner", "type": "address"}],
        "name": "nominateNewOwner",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "nominatedOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "proxy",
        "outputs": [{"internalType": "contract Proxy", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "rebuildCache",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolver",
        "outputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "",
                "type": "address",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolverAddressesRequired",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "addresses",
                "type": "bytes32[]",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_integrationProxy",
                "type": "address",
            }
        ],
        "name": "setIntegrationProxy",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "sender", "type": "address"}],
        "name": "setMessageSender",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_proxy",
                "type": "address",
            }
        ],
        "name": "setProxy",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "contract TokenState",
                "name": "_tokenState",
                "type": "address",
            }
        ],
        "name": "setTokenState",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "setTotalSupply",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "tokenState",
        "outputs": [
            {
                "internalType": "contract TokenState",
                "name": "",
                "type": "address",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transferAndSettle",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transferFromAndSettle",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "transferableSynths",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

rewards_escrow_v2_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "_owner", "type": "address"},
            {
                "internalType": "address",
                "name": "_resolver",
                "type": "address",
            },
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "accountToMerge",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "destinationAddress",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "escrowAmountMerged",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "entryIDs",
                "type": "uint256[]",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256",
            },
        ],
        "name": "AccountMerged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newDuration",
                "type": "uint256",
            }
        ],
        "name": "AccountMergingDurationUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "endTime",
                "type": "uint256",
            },
        ],
        "name": "AccountMergingStarted",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "entryIDs",
                "type": "uint256[]",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "escrowedAmountMigrated",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256",
            },
        ],
        "name": "BurnedForMigrationToL2",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "name",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "destination",
                "type": "address",
            },
        ],
        "name": "CacheUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "entryID",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "escrowAmount",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "endTime",
                "type": "uint256",
            },
        ],
        "name": "ImportedVestingEntry",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "escrowAmount",
                "type": "uint256",
            },
        ],
        "name": "ImportedVestingSchedule",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newDuration",
                "type": "uint256",
            }
        ],
        "name": "MaxAccountMergingDurationUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newDuration",
                "type": "uint256",
            }
        ],
        "name": "MaxEscrowDurationUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newAmount",
                "type": "uint256",
            }
        ],
        "name": "MigrateEntriesThresholdAmountUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "escrowedAmount",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "vestedAmount",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256",
            },
        ],
        "name": "MigratedAccountEscrow",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "destination",
                "type": "address",
            },
        ],
        "name": "NominateAccountToMerge",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldOwner",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnerChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            }
        ],
        "name": "OwnerNominated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "beneficiary",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Vested",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "beneficiary",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "duration",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "entryID",
                "type": "uint256",
            },
        ],
        "name": "VestingEntryCreated",
        "type": "event",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "acceptOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "accountMergingDuration",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "accountMergingIsOpen",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "accountMergingStartTime",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "name": "accountVestingEntryIDs",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "quantity", "type": "uint256"},
            {"internalType": "uint256", "name": "duration", "type": "uint256"},
        ],
        "name": "appendVestingEntry",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {
                "internalType": "uint256[]",
                "name": "entryIDs",
                "type": "uint256[]",
            },
        ],
        "name": "burnForMigration",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "escrowedAccountBalance",
                "type": "uint256",
            },
            {
                "components": [
                    {
                        "internalType": "uint64",
                        "name": "endTime",
                        "type": "uint64",
                    },
                    {
                        "internalType": "uint256",
                        "name": "escrowAmount",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct VestingEntries.VestingEntry[]",
                "name": "vestingEntries",
                "type": "tuple[]",
            },
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "beneficiary",
                "type": "address",
            },
            {"internalType": "uint256", "name": "deposit", "type": "uint256"},
            {"internalType": "uint256", "name": "duration", "type": "uint256"},
        ],
        "name": "createEscrowEntry",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "index", "type": "uint256"},
            {"internalType": "uint256", "name": "pageSize", "type": "uint256"},
        ],
        "name": "getAccountVestingEntryIDs",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "entryID", "type": "uint256"},
        ],
        "name": "getVestingEntry",
        "outputs": [
            {"internalType": "uint64", "name": "endTime", "type": "uint64"},
            {
                "internalType": "uint256",
                "name": "escrowAmount",
                "type": "uint256",
            },
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "entryID", "type": "uint256"},
        ],
        "name": "getVestingEntryClaimable",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {
                "internalType": "uint256[]",
                "name": "entryIDs",
                "type": "uint256[]",
            },
        ],
        "name": "getVestingQuantity",
        "outputs": [{"internalType": "uint256", "name": "total", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "index", "type": "uint256"},
            {"internalType": "uint256", "name": "pageSize", "type": "uint256"},
        ],
        "name": "getVestingSchedules",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint64",
                        "name": "endTime",
                        "type": "uint64",
                    },
                    {
                        "internalType": "uint256",
                        "name": "escrowAmount",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "entryID",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct VestingEntries.VestingEntryWithID[]",
                "name": "",
                "type": "tuple[]",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {
                "components": [
                    {
                        "internalType": "uint64",
                        "name": "endTime",
                        "type": "uint64",
                    },
                    {
                        "internalType": "uint256",
                        "name": "escrowAmount",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct VestingEntries.VestingEntry[]",
                "name": "",
                "type": "tuple[]",
            },
        ],
        "name": "importVestingEntries",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address[]",
                "name": "accounts",
                "type": "address[]",
            },
            {
                "internalType": "uint256[]",
                "name": "escrowAmounts",
                "type": "uint256[]",
            },
        ],
        "name": "importVestingSchedule",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "isResolverCached",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "maxAccountMergingDuration",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "max_duration",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "accountToMerge",
                "type": "address",
            },
            {
                "internalType": "uint256[]",
                "name": "entryIDs",
                "type": "uint256[]",
            },
        ],
        "name": "mergeAccount",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address[]",
                "name": "accounts",
                "type": "address[]",
            },
            {
                "internalType": "uint256[]",
                "name": "escrowBalances",
                "type": "uint256[]",
            },
            {
                "internalType": "uint256[]",
                "name": "vestedBalances",
                "type": "uint256[]",
            },
        ],
        "name": "migrateAccountEscrowBalances",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "migrateEntriesThresholdAmount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addressToMigrate",
                "type": "address",
            }
        ],
        "name": "migrateVestingSchedule",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "nextEntryId",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "nominateAccountToMerge",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "_owner", "type": "address"}],
        "name": "nominateNewOwner",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "nominatedOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "nominatedReceiver",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "numVestingEntries",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "rebuildCache",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolver",
        "outputs": [
            {
                "internalType": "contract AddressResolver",
                "name": "",
                "type": "address",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolverAddressesRequired",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "addresses",
                "type": "bytes32[]",
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "duration", "type": "uint256"}],
        "name": "setAccountMergingDuration",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "duration", "type": "uint256"}],
        "name": "setMaxAccountMergingWindow",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "duration", "type": "uint256"}],
        "name": "setMaxEscrowDuration",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "setMigrateEntriesThresholdAmount",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "setupExpiryTime",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "startMergingWindow",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "totalBalancePendingMigration",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "totalEscrowedAccountBalance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalEscrowedBalance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "totalVestedAccountBalance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint256[]",
                "name": "entryIDs",
                "type": "uint256[]",
            }
        ],
        "name": "vest",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "name": "vestingSchedules",
        "outputs": [
            {"internalType": "uint64", "name": "endTime", "type": "uint64"},
            {
                "internalType": "uint256",
                "name": "escrowAmount",
                "type": "uint256",
            },
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

liquidator_rewards_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "_owner", "type": "address"},
            {"internalType": "address", "name": "_resolver", "type": "address"},
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "name",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "destination",
                "type": "address",
            },
        ],
        "name": "CacheUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldOwner",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnerChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            }
        ],
        "name": "OwnerNominated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "user",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "reward",
                "type": "uint256",
            },
        ],
        "name": "RewardPaid",
        "type": "event",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "CONTRACT_NAME",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "acceptOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "accumulatedRewardsPerShare",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "earned",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "entries",
        "outputs": [
            {"internalType": "uint128", "name": "claimable", "type": "uint128"},
            {
                "internalType": "uint128",
                "name": "entryAccumulatedRewards",
                "type": "uint128",
            },
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "getReward",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "initiated",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "isResolverCached",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "_owner", "type": "address"}],
        "name": "nominateNewOwner",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "nominatedOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "reward", "type": "uint256"}],
        "name": "notifyRewardAmount",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "rebuildCache",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolver",
        "outputs": [
            {"internalType": "contract AddressResolver", "name": "", "type": "address"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "resolverAddressesRequired",
        "outputs": [
            {"internalType": "bytes32[]", "name": "addresses", "type": "bytes32[]"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "updateEntry",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
]
