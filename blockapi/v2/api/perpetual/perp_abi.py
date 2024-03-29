rewards_abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "_claimant",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_balance",
                "type": "uint256",
            },
        ],
        "name": "Claimed",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnershipTransferred",
        "type": "event",
    },
    {
        "inputs": [],
        "name": "candidate",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_liquidityProvider",
                "type": "address",
            },
            {"internalType": "uint256", "name": "_begin", "type": "uint256"},
            {"internalType": "uint256", "name": "_end", "type": "uint256"},
        ],
        "name": "claimStatus",
        "outputs": [{"internalType": "bool[]", "name": "", "type": "bool[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_account", "type": "address"},
            {"internalType": "uint256", "name": "_week", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "_claimedBalance",
                "type": "uint256",
            },
            {
                "internalType": "bytes32[]",
                "name": "_merkleProof",
                "type": "bytes32[]",
            },
        ],
        "name": "claimWeek",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_account", "type": "address"},
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "week",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "balance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "bytes32[]",
                        "name": "merkleProof",
                        "type": "bytes32[]",
                    },
                ],
                "internalType": "struct MerkleRedeemUpgradeSafe.Claim[]",
                "name": "_claims",
                "type": "tuple[]",
            },
        ],
        "name": "claimWeeks",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "address", "name": "", "type": "address"},
        ],
        "name": "claimed",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getLengthOfMerkleRoots",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "contract IERC20",
                "name": "_token",
                "type": "address",
            },
            {
                "internalType": "uint256",
                "name": "_vestingPeriod",
                "type": "uint256",
            },
        ],
        "name": "initialize",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "merkleRootIndexes",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "merkleRootTimestampMap",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_begin", "type": "uint256"},
            {"internalType": "uint256", "name": "_end", "type": "uint256"},
        ],
        "name": "merkleRoots",
        "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_week", "type": "uint256"},
            {
                "internalType": "bytes32",
                "name": "_merkleRoot",
                "type": "bytes32",
            },
            {
                "internalType": "uint256",
                "name": "_totalAllocation",
                "type": "uint256",
            },
        ],
        "name": "seedAllocations",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}],
        "name": "setOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "token",
        "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "updateOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_liquidityProvider",
                "type": "address",
            },
            {"internalType": "uint256", "name": "_week", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "_claimedBalance",
                "type": "uint256",
            },
            {
                "internalType": "bytes32[]",
                "name": "_merkleProof",
                "type": "bytes32[]",
            },
        ],
        "name": "verifyClaim",
        "outputs": [{"internalType": "bool", "name": "valid", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "vestingPeriod",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "weekMerkleRoots",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
]
