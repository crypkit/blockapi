# CHANGELOG


## v0.59.1 (2025-04-24)

### Bug Fixes

- **unisat**: Offers collection_id rename to collection
  ([`e10a944`](https://github.com/crypkit/blockapi/commit/e10a944592dcad505f8b8f689568d104edba9d27))


## v0.59.0 (2025-04-15)

### Features

- Implement Unisat API for BTC NFTs; fetch NFTs, collections, offers, listings
  ([`b5a5684`](https://github.com/crypkit/blockapi/commit/b5a56848250a28033c3325dc491e547d58814c4e))


## v0.58.0 (2025-04-15)


## v0.57.0 (2025-04-10)

### Features

- Implement Unisat API for BTC NFTs; fetch NFTs, collections, offers, listings
  ([`afc76a8`](https://github.com/crypkit/blockapi/commit/afc76a85b98e3e2219d827b497bc23a00528453c))

- Implement Unisat API for BTC NFTs; fetch NFTs, collections, offers, listings
  ([`6c0b63a`](https://github.com/crypkit/blockapi/commit/6c0b63a82c02e07fd620a954bd547f01ecc4dd51))


## v0.56.0 (2025-03-19)

### Features

- Add new blockchain mappings and enum definitions (Abstract, Berachain, Story and Unichain)
  ([`d0284a2`](https://github.com/crypkit/blockapi/commit/d0284a2fccc20b5c532ade128f3e9db979fc0b6a))

- Formatting?
  ([`f9a5b72`](https://github.com/crypkit/blockapi/commit/f9a5b72db74dbf8373880e480663a5764dad9a11))


## v0.55.0 (2025-02-21)

### Bug Fixes

- Fix Enum to (str, Enum)
  ([`c794fc3`](https://github.com/crypkit/blockapi/commit/c794fc3eb2e29ad8709bf057a233de21e8dcd23a))

### Features

- Add order_by arg to offers and listings endpoints
  ([`e4210a6`](https://github.com/crypkit/blockapi/commit/e4210a6b818179299d35c5bda423b3fee1ea31f7))


## v0.54.3 (2025-02-04)

### Bug Fixes

- **debank**: Ignore duplicate symbols in asset import list
  ([#222](https://github.com/crypkit/blockapi/pull/222),
  [`8969ad6`](https://github.com/crypkit/blockapi/commit/8969ad63551523f547b101a0dadd011784e97261))


## v0.54.2 (2025-02-03)

### Bug Fixes

- Don't import negative balances ([#221](https://github.com/crypkit/blockapi/pull/221),
  [`26f68ad`](https://github.com/crypkit/blockapi/commit/26f68ade139dd79c4198be06bdcbbc71cf674573))


## v0.54.1 (2025-01-30)

### Bug Fixes

- Removed solana main
  ([`e527122`](https://github.com/crypkit/blockapi/commit/e527122dfef051536a7382324883aecdf214f6f0))


## v0.54.0 (2025-01-30)

### Features

- Solana: checking tokenmap responses + added ENVs for override
  ([`d2b905e`](https://github.com/crypkit/blockapi/commit/d2b905eaaaf288efd0ece4825d80d8cb8e6be8bb))


## v0.53.0 (2025-01-29)

### Features

- Set project homepage
  ([`f962d23`](https://github.com/crypkit/blockapi/commit/f962d2395a2222e8712d2c1e8c1f0fc2362f1598))


## v0.52.1 (2025-01-29)

### Bug Fixes

- Bio: fix bio pools parsing
  ([`02f81a5`](https://github.com/crypkit/blockapi/commit/02f81a50591c6877abb6416f213f999017277ba2))


## v0.52.0 (2025-01-23)

### Features

- Add Rune support ([#216](https://github.com/crypkit/blockapi/pull/216),
  [`6ea7cac`](https://github.com/crypkit/blockapi/commit/6ea7cacdd18e11b9471ed7129a2c6b42a35b9806))

* feat: Add Rune support

* fix test


## v0.51.3 (2024-12-18)

### Bug Fixes

- Update blockchain list ([#215](https://github.com/crypkit/blockapi/pull/215),
  [`09d020a`](https://github.com/crypkit/blockapi/commit/09d020a4036687aa3a489aa07675b9e99d16b5b1))


## v0.51.2 (2024-12-11)

### Bug Fixes

- Sui: sleep 10s between requests
  ([`fb5e0b9`](https://github.com/crypkit/blockapi/commit/fb5e0b9078e13aa207875c07f55c4980e73d1af7))


## v0.51.1 (2024-12-06)

### Bug Fixes

- Sui: switched to balances endpoint '/sui/v1/accounts/{address}/balance'
  ([`2372def`](https://github.com/crypkit/blockapi/commit/2372defb31ad1c4047416a6264e511a53229a98d))


## v0.51.0 (2024-11-15)

### Features

- Sui: format address without leading '0'
  ([`64e7910`](https://github.com/crypkit/blockapi/commit/64e7910b9bb00ed298526942e6021df0b8f8f3f3))


## v0.50.1 (2024-11-14)

### Bug Fixes

- Sui parsing after api base change
  ([`dfb90f0`](https://github.com/crypkit/blockapi/commit/dfb90f00f0872e65ead9d5ade892d93dc492d722))


## v0.50.0 (2024-11-14)

### Features

- Switch sui to blockberry api
  ([`ebdebf2`](https://github.com/crypkit/blockapi/commit/ebdebf2fa92d9f9b7843abfa924f70b2ecb95a87))


## v0.49.5 (2024-11-11)

### Bug Fixes

- Sui balances fetching
  ([`65bd81a`](https://github.com/crypkit/blockapi/commit/65bd81aaba13753b8bcc4f7cc18984dcdab8f9e0))


## v0.49.4 (2024-11-06)

### Bug Fixes

- Solana token mapping
  ([`e469995`](https://github.com/crypkit/blockapi/commit/e469995f3959a74fb715eed17cbb545251d106de))


## v0.49.3 (2024-11-06)

### Bug Fixes

- Fetch coins later ([#207](https://github.com/crypkit/blockapi/pull/207),
  [`8895464`](https://github.com/crypkit/blockapi/commit/8895464005cbc707c86c4ffe6c7ce717ed8bffbb))


## v0.49.2 (2024-11-04)

### Bug Fixes

- Sui coin address with all "::" suffixes (shortform)
  ([`47890fe`](https://github.com/crypkit/blockapi/commit/47890fe0e38e3643defcaeedc9089ba963328cc8))


## v0.49.1 (2024-10-31)

### Bug Fixes

- Fix build imports
  ([`8e8d04d`](https://github.com/crypkit/blockapi/commit/8e8d04d05cef724c732d93519fba88648e04585c))


## v0.49.0 (2024-10-30)

### Features

- Add SUI API
  ([`8c43d8b`](https://github.com/crypkit/blockapi/commit/8c43d8bd196733d3ea60e7cd864dac32fd742541))


## v0.48.5 (2024-10-23)

### Bug Fixes

- **Solana**: When fetching meme coin details ignore malformed data
  ([#203](https://github.com/crypkit/blockapi/pull/203),
  [`dd566a2`](https://github.com/crypkit/blockapi/commit/dd566a22d2411acf3e8211051f50e5fa934a201e))


## v0.48.4 (2024-10-22)

### Bug Fixes

- Ignore data from IPFS if not responding ([#202](https://github.com/crypkit/blockapi/pull/202),
  [`cc8b2d4`](https://github.com/crypkit/blockapi/commit/cc8b2d41079dea10b7ad2ebe64579a391095b661))


## v0.48.3 (2024-10-22)

### Bug Fixes

- Fetch token data from metaplex if not in list
  ([#201](https://github.com/crypkit/blockapi/pull/201),
  [`db58cdc`](https://github.com/crypkit/blockapi/commit/db58cdc51674daea1ade2be22b4b971688c18c3b))


## v0.48.2 (2024-09-11)

### Bug Fixes

- Nft collection name ([#200](https://github.com/crypkit/blockapi/pull/200),
  [`e421814`](https://github.com/crypkit/blockapi/commit/e4218147271822e4f44f8d628cb33ed1948b3701))


## v0.48.1 (2024-08-07)

### Bug Fixes

- Fix reqs
  ([`7db17da`](https://github.com/crypkit/blockapi/commit/7db17da79e700aa1d269fbda6e3b4b9597a4d139))

- Fix sonarwatch tokenlist
  ([`bc06022`](https://github.com/crypkit/blockapi/commit/bc06022b55ded6096e125f9f0a260bddde4171ed))


## v0.48.0 (2024-07-24)

### Features

- Add support and mapping for new blockchains ([#198](https://github.com/crypkit/blockapi/pull/198),
  [`3a5698d`](https://github.com/crypkit/blockapi/commit/3a5698d9b69412226174fa23026ddb580ec20ce4))


## v0.47.1 (2024-07-11)

### Bug Fixes

- Handling requests ConnectionError (instead of buildin) in CustomizableBlockchainApi.get_data
  ([`fe16722`](https://github.com/crypkit/blockapi/commit/fe1672273d3b389d15ea02a1a355668936fa20cd))


## v0.47.0 (2024-07-09)

### Features

- Handle ConnectionError in CustomizableBlockchainApi.get_data
  ([`3db6e22`](https://github.com/crypkit/blockapi/commit/3db6e22b359ec0b239036688e65ba8c7c484a028))


## v0.46.0 (2024-07-04)

### Features

- Added logging to 'get_data' method to investigate SOL fetching errors
  ([`23cb3a0`](https://github.com/crypkit/blockapi/commit/23cb3a04d6b5eb1314f0517e0d4c55fb0f114e08))


## v0.45.3 (2024-06-06)

### Bug Fixes

- Update known blockchains ([#194](https://github.com/crypkit/blockapi/pull/194),
  [`b163e19`](https://github.com/crypkit/blockapi/commit/b163e197eea820a24c9cafd3d5aa9ae1cc5cc527))


## v0.45.2 (2024-05-30)

### Bug Fixes

- Update list of known blockchains ([#193](https://github.com/crypkit/blockapi/pull/193),
  [`4dc23a0`](https://github.com/crypkit/blockapi/commit/4dc23a0b5fa8c4bbd9e09c2e67ca5ddce8dd4c9a))


## v0.45.1 (2024-05-29)

### Bug Fixes

- Change rent_reserve type to locked
  ([`df1d2be`](https://github.com/crypkit/blockapi/commit/df1d2bef5dd5d9dd08804b65518c83a57e9ec080))


## v0.45.0 (2024-05-29)

### Bug Fixes

- Formatting
  ([`e0fbb6f`](https://github.com/crypkit/blockapi/commit/e0fbb6f853415f6bdd21dd091ed2dc8917b5ea4d))

### Features

- Add staking rent reserve balance for solana
  ([`43b5702`](https://github.com/crypkit/blockapi/commit/43b5702ee538360ccedc5aa0366432a561792576))


## v0.44.0 (2024-05-27)

### Chores

- **deps**: Bump requests from 2.31.0 to 2.32.0
  ([#188](https://github.com/crypkit/blockapi/pull/188),
  [`13b1fc4`](https://github.com/crypkit/blockapi/commit/13b1fc444e6505d679b2a65bb0189c799c4da131))

updated-dependencies: - dependency-name: requests dependency-type: direct:production ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Features

- Add stake balance for solana
  ([`22a1951`](https://github.com/crypkit/blockapi/commit/22a1951e8d7e5631441ebbc56721eabfd0f96989))


## v0.43.0 (2024-05-24)

### Bug Fixes

- Fix imports
  ([`d2565e5`](https://github.com/crypkit/blockapi/commit/d2565e53aa332ed6440bd7688be1fbde0da0c701))

- Fix unittests
  ([`dbe48ee`](https://github.com/crypkit/blockapi/commit/dbe48eebac83bed09a1679c80e0860a1601aacd1))

### Features

- Add more solana token lists
  ([`6cb65ae`](https://github.com/crypkit/blockapi/commit/6cb65ae5e41deb1ad587d184bc2291f60ea2f1f4))


## v0.42.3 (2024-04-25)

### Bug Fixes

- Improve Solana token mapping ([#187](https://github.com/crypkit/blockapi/pull/187),
  [`9284176`](https://github.com/crypkit/blockapi/commit/9284176f64258a1faf09ceadf6c0c1f75339f2e9))


## v0.42.2 (2024-03-20)

### Bug Fixes

- Parse non-native tokens ([#186](https://github.com/crypkit/blockapi/pull/186),
  [`4f08d06`](https://github.com/crypkit/blockapi/commit/4f08d0683d0679b5f6ec4fc82247b0e20a412c3c))


## v0.42.1 (2024-03-19)

### Bug Fixes

- Simplehash: Fetch all chains at the same time
  ([#185](https://github.com/crypkit/blockapi/pull/185),
  [`419b2da`](https://github.com/crypkit/blockapi/commit/419b2da5ebf39edbf9832ff0316b0325f78868ec))


## v0.42.0 (2024-03-15)

### Features

- Add pending_transaction asset type
  ([`c03f335`](https://github.com/crypkit/blockapi/commit/c03f335c2439b91da13070b9b385bcb319ad0d00))


## v0.41.0 (2024-03-12)

### Features

- Bump 'coinaddrng' to '1.1.1'
  ([`5315052`](https://github.com/crypkit/blockapi/commit/53150526f3bf3c75627eb20389a27875eed55bab))


## v0.40.8 (2024-03-07)

### Bug Fixes

- Add new blockchains and mapping ([#182](https://github.com/crypkit/blockapi/pull/182),
  [`9e834d3`](https://github.com/crypkit/blockapi/commit/9e834d398e5a4b939580f0ebaa3ffc26fb17ae8e))


## v0.40.7 (2024-03-06)

### Bug Fixes

- Empty collection activity ([#181](https://github.com/crypkit/blockapi/pull/181),
  [`63615d4`](https://github.com/crypkit/blockapi/commit/63615d45f07671662a0e9d940bc129ff262d216c))


## v0.40.6 (2024-03-06)

### Bug Fixes

- Simplehash: Add default volumes if none is available
  ([`4a004b1`](https://github.com/crypkit/blockapi/commit/4a004b1129ad1b0a9d1df331fc93db2f9a32c9f4))


## v0.40.5 (2024-02-29)

### Bug Fixes

- Automatically delay and refetch if 429 ([#177](https://github.com/crypkit/blockapi/pull/177),
  [`11ad0aa`](https://github.com/crypkit/blockapi/commit/11ad0aa2de4bcafb25d328b2ee21832279d2571e))


## v0.40.4 (2024-02-29)

### Bug Fixes

- Include listed tokens in fetch ([#179](https://github.com/crypkit/blockapi/pull/179),
  [`b229c1e`](https://github.com/crypkit/blockapi/commit/b229c1ee4da9ba8e492c72a811ca42c870d8c972))


## v0.40.3 (2024-02-29)

### Bug Fixes

- Best offers field name ([#178](https://github.com/crypkit/blockapi/pull/178),
  [`162ad17`](https://github.com/crypkit/blockapi/commit/162ad174d9698076a0c4e2be58c999cbc85d4efb))


## v0.40.2 (2024-02-28)

### Bug Fixes

- Disable Klaytn on SimpleHash
  ([`6ec846c`](https://github.com/crypkit/blockapi/commit/6ec846c02f8b5ff203981ec700b962e58f9f1cc5))


## v0.40.1 (2024-02-28)

### Bug Fixes

- Make more effort do find collection name ([#176](https://github.com/crypkit/blockapi/pull/176),
  [`a89b963`](https://github.com/crypkit/blockapi/commit/a89b963694d51bff6ca32035b9cba955e6414efb))


## v0.40.0 (2024-02-27)

### Features

- Fetch NFTs from Simple Hash ([#175](https://github.com/crypkit/blockapi/pull/175),
  [`ab5b258`](https://github.com/crypkit/blockapi/commit/ab5b258e09e44e9e6a07629b17aefc0c611ceeaa))


## v0.39.0 (2024-02-22)

### Features

- Fix retry logic for OpenSea ([#174](https://github.com/crypkit/blockapi/pull/174),
  [`cfbf0d1`](https://github.com/crypkit/blockapi/commit/cfbf0d14e5b986ae1714bc9e3e002e1c232d4eb5))


## v0.38.0 (2024-02-20)

### Features

- Fetch BTC NFT ([#173](https://github.com/crypkit/blockapi/pull/173),
  [`60d81e7`](https://github.com/crypkit/blockapi/commit/60d81e772802ef34b9ddebc20fa167396844f0a6))


## v0.37.5 (2024-02-19)

### Bug Fixes

- Improve Magic Eden retry logic ([#172](https://github.com/crypkit/blockapi/pull/172),
  [`8719d5f`](https://github.com/crypkit/blockapi/commit/8719d5f7e0ccfc3a60b2cd0d578af35f4a502658))


## v0.37.4 (2024-02-16)

### Bug Fixes

- Ignore zero listing and skip duplicates ([#171](https://github.com/crypkit/blockapi/pull/171),
  [`5ef1fc9`](https://github.com/crypkit/blockapi/commit/5ef1fc9e1f9f1b91f838a1963e0a0e217d5396d8))


## v0.37.3 (2024-02-16)

### Bug Fixes

- Add MATIC mapping ([#170](https://github.com/crypkit/blockapi/pull/170),
  [`9fcdafa`](https://github.com/crypkit/blockapi/commit/9fcdafa8c3bb9f5f248fa863d8ac59640f1e51e2))


## v0.37.2 (2024-02-14)

### Bug Fixes

- Offer fetching and price ([#169](https://github.com/crypkit/blockapi/pull/169),
  [`e2ae9fa`](https://github.com/crypkit/blockapi/commit/e2ae9fa8389a349c12043448953b1958b4532df4))


## v0.37.1 (2024-02-12)

### Bug Fixes

- Use default values for collection stats ([#168](https://github.com/crypkit/blockapi/pull/168),
  [`483b5a1`](https://github.com/crypkit/blockapi/commit/483b5a19e60670512baa9831bd15ff8033451780))


## v0.37.0 (2024-02-10)

### Features

- Fetch Solana NFT ([#167](https://github.com/crypkit/blockapi/pull/167),
  [`9e390d8`](https://github.com/crypkit/blockapi/commit/9e390d8ad08fe3cc07067f28805b184ebea9b261))


## v0.36.0 (2024-02-07)

### Chores

- Black update and reformat ([#166](https://github.com/crypkit/blockapi/pull/166),
  [`1dfc448`](https://github.com/crypkit/blockapi/commit/1dfc4482d90bb6b9a683140303c4c157816c5306))

### Features

- Support multiple OpenSea blockchains ([#165](https://github.com/crypkit/blockapi/pull/165),
  [`657d697`](https://github.com/crypkit/blockapi/commit/657d69762b63ce4bc6be027befaa87e145917658))


## v0.35.1 (2024-01-23)

### Bug Fixes

- Ocmosis: fix Osmosis decimals
  ([`bfc48fa`](https://github.com/crypkit/blockapi/commit/bfc48fa70c34593907d7a35685daa16bcefaeefb))


## v0.35.0 (2024-01-19)

### Bug Fixes

- Cosmos: return original denom always
  ([`9e13025`](https://github.com/crypkit/blockapi/commit/9e130258caf67b90ea0e1c991b6ffa0f198e1e27))

### Features

- Cosmos rewards fix (not use just the first reward)
  ([`12de4e9`](https://github.com/crypkit/blockapi/commit/12de4e96e3a5e56811477bf851d9e5b640fef55d))

- Cosmos uses pulsar IBC Token Data
  ([`9cbbd16`](https://github.com/crypkit/blockapi/commit/9cbbd160820ff0c3d4597b37195143b510ffa158))

- Cosmos: added dydx, celestia
  ([`1c558cb`](https://github.com/crypkit/blockapi/commit/1c558cb6a92af1a6150e18676a3f3c7b4a4793db))

- Cosmos: added osmosis, dydx, celestia
  ([`a7bd515`](https://github.com/crypkit/blockapi/commit/a7bd515c72997dc95d6de853dcbbfc8144780b7c))

- Refactoring: split token map loading into a separate class
  ([`131efe1`](https://github.com/crypkit/blockapi/commit/131efe122b2c972bc0173bf90a9f0811c3fdfc11))


## v0.34.0 (2024-01-16)

### Features

- [solana] Also fetch Token 2022 SPLs ([#162](https://github.com/crypkit/blockapi/pull/162),
  [`91fbce6`](https://github.com/crypkit/blockapi/commit/91fbce6fa992dd13f787d4ca0739c660e6f39270))


## v0.33.0 (2024-01-11)

### Features

- Add support for new blockchains ([#161](https://github.com/crypkit/blockapi/pull/161),
  [`a6c815a`](https://github.com/crypkit/blockapi/commit/a6c815a788c1b845273c1fa2ade31d1a34592c1b))


## v0.32.0 (2023-12-13)

### Features

- Fetch NFTs iteratively ([#160](https://github.com/crypkit/blockapi/pull/160),
  [`8172763`](https://github.com/crypkit/blockapi/commit/8172763a546455425d4e81ffaace625ab45f9a20))


## v0.31.3 (2023-12-08)

### Bug Fixes

- [opensea] Parse multiple contracts for collection
  ([#159](https://github.com/crypkit/blockapi/pull/159),
  [`fdc40e8`](https://github.com/crypkit/blockapi/commit/fdc40e8a53373439ddff83d086972aca9baa2e27))


## v0.31.2 (2023-12-08)

### Bug Fixes

- Blockchair fetch error ([#158](https://github.com/crypkit/blockapi/pull/158),
  [`7b30a1a`](https://github.com/crypkit/blockapi/commit/7b30a1a132e300c71585912eaddd148c3f69cf25))


## v0.31.1 (2023-12-08)

### Bug Fixes

- [opensea] Get correct listing price ([#157](https://github.com/crypkit/blockapi/pull/157),
  [`6e8d4c4`](https://github.com/crypkit/blockapi/commit/6e8d4c4136a2160d60e58942d616ed1a79ec3a2b))


## v0.31.0 (2023-12-04)

### Features

- Limit NFT fetches and return cursor ([#156](https://github.com/crypkit/blockapi/pull/156),
  [`56a0857`](https://github.com/crypkit/blockapi/commit/56a085765ac066cd71abd843ebe616c5201e029f))


## v0.30.5 (2023-11-29)

### Bug Fixes

- Parse NFT collection when there is no base symbol
  ([#155](https://github.com/crypkit/blockapi/pull/155),
  [`b8f6435`](https://github.com/crypkit/blockapi/commit/b8f643515517d637247b22f45c92d875fb623108))


## v0.30.4 (2023-11-22)

### Bug Fixes

- Blockchair and Debank parsing ([#154](https://github.com/crypkit/blockapi/pull/154),
  [`c723d50`](https://github.com/crypkit/blockapi/commit/c723d5034eb94ce9407ed692a71331e12ebbdfcc))


## v0.30.3 (2023-11-14)

### Bug Fixes

- Change solana token list source ([#152](https://github.com/crypkit/blockapi/pull/152),
  [`6babc47`](https://github.com/crypkit/blockapi/commit/6babc470d821d7234b07c4a4b2731fe4b1e032ce))


## v0.30.2 (2023-11-14)

### Bug Fixes

- Return error when source closes connection ([#151](https://github.com/crypkit/blockapi/pull/151),
  [`8e7c9ce`](https://github.com/crypkit/blockapi/commit/8e7c9ce5173db6bbea5f0e9981b3a6806c4cd72b))


## v0.30.1 (2023-11-10)

### Bug Fixes

- Add Opensea coin mapping ([#150](https://github.com/crypkit/blockapi/pull/150),
  [`821f026`](https://github.com/crypkit/blockapi/commit/821f02615d922e051b76c7a11c0de79349d186d4))


## v0.30.0 (2023-11-09)

### Features

- Fetch multiple pages of NFT offers, add key and blockchain
  ([#149](https://github.com/crypkit/blockapi/pull/149),
  [`74b0528`](https://github.com/crypkit/blockapi/commit/74b0528623ce5b8b5be715aa0d53d5281f5238ae))


## v0.29.1 (2023-10-27)

### Bug Fixes

- Enum values for NFT offer type ([#148](https://github.com/crypkit/blockapi/pull/148),
  [`78df014`](https://github.com/crypkit/blockapi/commit/78df014503886554568fbbdf44d8aa8213b5f619))


## v0.29.0 (2023-10-25)

### Features

- Opensea - Parse collection contract ([#147](https://github.com/crypkit/blockapi/pull/147),
  [`61a1646`](https://github.com/crypkit/blockapi/commit/61a1646b3d77d259610edfb7def3c78119a68b4c))


## v0.28.0 (2023-10-20)

### Features

- Fetch NFT from OpenSea ([#146](https://github.com/crypkit/blockapi/pull/146),
  [`edc1ffa`](https://github.com/crypkit/blockapi/commit/edc1ffa6d2f9af42eac77c3f8236e64421817097))


## v0.27.2 (2023-09-29)

### Bug Fixes

- Build correct URL when using POST ([#145](https://github.com/crypkit/blockapi/pull/145),
  [`4eea5b2`](https://github.com/crypkit/blockapi/commit/4eea5b230e87f980e3e73180dbd6db231c839bbf))


## v0.27.1 (2023-09-13)

### Bug Fixes

- Don't detect errors on empty portfolio ([#144](https://github.com/crypkit/blockapi/pull/144),
  [`157da4a`](https://github.com/crypkit/blockapi/commit/157da4a4ee4ce0d6166c75b7c95eb2f08ea210a5))

### Chores

- Run CI only once when merging branch ([#143](https://github.com/crypkit/blockapi/pull/143),
  [`38b2db5`](https://github.com/crypkit/blockapi/commit/38b2db5ed532a25255b3a65b0768e3b37cf569c1))


## v0.27.0 (2023-09-11)

### Features

- Add new coingecko platforms mapping ([#142](https://github.com/crypkit/blockapi/pull/142),
  [`f96424d`](https://github.com/crypkit/blockapi/commit/f96424deef055a7deb0a4a8b7a70fdc9ff8d30d5))


## v0.26.3 (2023-09-01)

### Bug Fixes

- Remove unusable web3 limiter method ([#141](https://github.com/crypkit/blockapi/pull/141),
  [`610e592`](https://github.com/crypkit/blockapi/commit/610e5928ba8bc02c971467b379b1b8eb58e983e1))


## v0.26.2 (2023-09-01)

### Bug Fixes

- Add tests for fetchers ([#140](https://github.com/crypkit/blockapi/pull/140),
  [`fb205f5`](https://github.com/crypkit/blockapi/commit/fb205f588bcc4e564b9db056686fd8a229602fa8))

### Chores

- **deps**: Bump requests from 2.28.1 to 2.31.0
  ([#124](https://github.com/crypkit/blockapi/pull/124),
  [`1e74df9`](https://github.com/crypkit/blockapi/commit/1e74df9f7d00c24cec8dcc4da5f5a89363a13d4f))

Bumps [requests](https://github.com/psf/requests) from 2.28.1 to 2.31.0. - [Release
  notes](https://github.com/psf/requests/releases) -
  [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md) -
  [Commits](https://github.com/psf/requests/compare/v2.28.1...v2.31.0)

--- updated-dependencies: - dependency-name: requests dependency-type: direct:production ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>


## v0.26.1 (2023-08-30)

### Bug Fixes

- Add blockchains and mapping ([#139](https://github.com/crypkit/blockapi/pull/139),
  [`bf20508`](https://github.com/crypkit/blockapi/commit/bf20508a80ebca1b748f5eacb3c1b04b712759e1))

Co-authored-by: galvanizze <marek.galvanek@gmail.com>


## v0.26.0 (2023-08-23)

### Features

- Refactor Debank fetching and parsing ([#138](https://github.com/crypkit/blockapi/pull/138),
  [`fd7cb8c`](https://github.com/crypkit/blockapi/commit/fd7cb8ce82d11406bc1686d3de431dbf04675a5c))


## v0.25.0 (2023-08-17)

### Features

- Improve V2 interface ([#131](https://github.com/crypkit/blockapi/pull/131),
  [`133123d`](https://github.com/crypkit/blockapi/commit/133123d07f141483429ca2b8f26d1702be406907))


## v0.24.2 (2023-07-31)

### Bug Fixes

- **debank**: Pool fields availability ([#137](https://github.com/crypkit/blockapi/pull/137),
  [`89498f9`](https://github.com/crypkit/blockapi/commit/89498f93469c204e0a3ad623003ffb2cfa461290))


## v0.24.1 (2023-07-28)

### Bug Fixes

- **debank**: Remove unused TokenRole ([#135](https://github.com/crypkit/blockapi/pull/135),
  [`fbf9d17`](https://github.com/crypkit/blockapi/commit/fbf9d170f920fdf9e86bceccebf77c54793b9675))

- **release**: Don't fail if no tag is present
  ([#136](https://github.com/crypkit/blockapi/pull/136),
  [`3b55c19`](https://github.com/crypkit/blockapi/commit/3b55c192da14942ca8955a67a4e7e0bd16292168))

### Chores

- **ci**: Fix semantic release configuration ([#134](https://github.com/crypkit/blockapi/pull/134),
  [`e82d901`](https://github.com/crypkit/blockapi/commit/e82d90171d57585a059faabe3dfdeb869889e50c))


## v0.24.0 (2023-07-28)

### Chores

- **ci**: Fix semantic-release version detection
  ([#133](https://github.com/crypkit/blockapi/pull/133),
  [`eee8f33`](https://github.com/crypkit/blockapi/commit/eee8f3312e621f3a06bf39beeeb99f3477887a2a))

### Features

- **debank**: Add PoolInfo ([#132](https://github.com/crypkit/blockapi/pull/132),
  [`589026c`](https://github.com/crypkit/blockapi/commit/589026cb005c70ec629fd68343defd9e67c8f6e6))


## v0.23.0 (2023-07-14)

### Features

- Move token list to Pool ([#130](https://github.com/crypkit/blockapi/pull/130),
  [`436d765`](https://github.com/crypkit/blockapi/commit/436d765575e0a36d9e572dcbe89c3011d4d7beb5))


## v0.22.0 (2023-07-13)

### Chores

- **debank**: Add default values for pydantic optional fields
  ([#129](https://github.com/crypkit/blockapi/pull/129),
  [`2eeae2b`](https://github.com/crypkit/blockapi/commit/2eeae2b627cb0cb063f5025d6ebeccd6900f9ba4))

### Features

- Add pending_transaction asset type
  ([`68e9abf`](https://github.com/crypkit/blockapi/commit/68e9abfe24a1fb96074b3160451ffb2b9b5e5c8a))


## v0.21.3 (2023-05-31)

### Bug Fixes

- Trezorlitecoinapi base coin ([#126](https://github.com/crypkit/blockapi/pull/126),
  [`a5b9fef`](https://github.com/crypkit/blockapi/commit/a5b9fefda158b2a2005b4a6c176d5accb1aae455))


## v0.21.2 (2023-05-22)

### Bug Fixes

- Disable Solana staking endpoint ([#123](https://github.com/crypkit/blockapi/pull/123),
  [`ed2b9f3`](https://github.com/crypkit/blockapi/commit/ed2b9f3f9a8a19fa470ffeabdeedddc5571c8995))


## v0.21.1 (2023-05-16)

### Bug Fixes

- Fix requirements
  ([`c453850`](https://github.com/crypkit/blockapi/commit/c453850bacfc9df40760b1add714cd80fa01a157))


## v0.21.0 (2023-05-16)

### Features

- Fetch blockchains from debank
  ([`b2246eb`](https://github.com/crypkit/blockapi/commit/b2246eb8191b2f7a93cb3b10ce541b2b0fe1fb85))

- Fix requirements
  ([`5ce61c0`](https://github.com/crypkit/blockapi/commit/5ce61c03bbe7bbd02503d14395dcb949b6abb928))

- Fix requirements
  ([`eae7aa0`](https://github.com/crypkit/blockapi/commit/eae7aa0157217cc9570d0cc12dc235f12eae8682))


## v0.20.0 (2023-04-24)

### Features

- Add solana staked balance
  ([`828df57`](https://github.com/crypkit/blockapi/commit/828df576a1146faea273bf469dba7af7d49ffcbf))


## v0.19.4 (2023-04-20)

### Bug Fixes

- **TrezorApi**: Send UA in headers ([#120](https://github.com/crypkit/blockapi/pull/120),
  [`316cf24`](https://github.com/crypkit/blockapi/commit/316cf247f79776967f7227de9f1b51ba89c76524))


## v0.19.3 (2023-04-14)

### Bug Fixes

- **coingecko**: Oasis chain mapping ([#119](https://github.com/crypkit/blockapi/pull/119),
  [`1e69514`](https://github.com/crypkit/blockapi/commit/1e6951436eea7360f43577c5e74173f3e5a665e6))


## v0.19.2 (2023-04-14)

### Bug Fixes

- Debank portfolio parse crash on unknown chain
  ([#118](https://github.com/crypkit/blockapi/pull/118),
  [`57a4322`](https://github.com/crypkit/blockapi/commit/57a432245e9f7b73279f2b37e0c686d451ebee19))


## v0.19.1 (2023-04-13)

### Bug Fixes

- **debank, coingecko**: Add blockchains and mapping
  ([#117](https://github.com/crypkit/blockapi/pull/117),
  [`368ec1d`](https://github.com/crypkit/blockapi/commit/368ec1d251e647faf6468937bc222eaae5898335))


## v0.19.0 (2023-04-13)

### Features

- Add V2 Bitcoin Trezor API ([#116](https://github.com/crypkit/blockapi/pull/116),
  [`e82c4b8`](https://github.com/crypkit/blockapi/commit/e82c4b8260684d577fdada4bad8fdfce8f1705fc))


## v0.18.0 (2023-04-04)

### Features

- Synthetix: AssetType.STAKED contains collateral.
  ([`f8e73a8`](https://github.com/crypkit/blockapi/commit/f8e73a8510fc539e6ff815cd88b77275c8530e31))


## v0.17.1 (2023-03-23)

### Bug Fixes

- Perpetual not fetching data ([#114](https://github.com/crypkit/blockapi/pull/114),
  [`f0fdf79`](https://github.com/crypkit/blockapi/commit/f0fdf79d39d5376a7494154e246570e505486cc9))


## v0.17.0 (2023-03-21)

### Chores

- Update pre-commit dependencies to current versions
  ([#111](https://github.com/crypkit/blockapi/pull/111),
  [`c0efb21`](https://github.com/crypkit/blockapi/commit/c0efb2117ad62d3bfb96169a86030c8da237f31b))

### Features

- **debank**: Add usage endpoint ([#113](https://github.com/crypkit/blockapi/pull/113),
  [`cc295d3`](https://github.com/crypkit/blockapi/commit/cc295d36b84e7ac80eea53f31b105149f84408d2))


## v0.16.1 (2023-03-21)

### Bug Fixes

- Limit web3 version ([#112](https://github.com/crypkit/blockapi/pull/112),
  [`4260ea9`](https://github.com/crypkit/blockapi/commit/4260ea956f1156a150826c3df45052afe8affc73))


## v0.16.0 (2023-03-08)

### Features

- Add position_index to distinguish reused LPs
  ([#110](https://github.com/crypkit/blockapi/pull/110),
  [`6ab1a27`](https://github.com/crypkit/blockapi/commit/6ab1a272caffb98ea81e06b2d85ddb3b5a37c0c1))


## v0.15.5 (2023-03-03)

### Bug Fixes

- Different AssetType for rewards for LP and Locked assets
  ([`b0793ba`](https://github.com/crypkit/blockapi/commit/b0793ba3b9de6725ff125911fbdfadcd65bafff2))


## v0.15.4 (2023-02-22)

### Bug Fixes

- Parse Aurora AETH ([#109](https://github.com/crypkit/blockapi/pull/109),
  [`4e0b3a1`](https://github.com/crypkit/blockapi/commit/4e0b3a173b5c2352c6f2bc3f4135ad3ab1172905))


## v0.15.3 (2023-02-15)

### Bug Fixes

- Add AssetType Priced Vesting ([#108](https://github.com/crypkit/blockapi/pull/108),
  [`95c140c`](https://github.com/crypkit/blockapi/commit/95c140cb5d5948ddfa56b1c9365de7f00f9a85c1))


## v0.15.2 (2023-02-13)

### Bug Fixes

- Update AssetTypes ([#107](https://github.com/crypkit/blockapi/pull/107),
  [`858f942`](https://github.com/crypkit/blockapi/commit/858f94235c954bfeb9ed04c734b3719275f3055b))


## v0.15.1 (2023-02-13)

### Bug Fixes

- Parse pool name from description if provided
  ([#106](https://github.com/crypkit/blockapi/pull/106),
  [`240ed21`](https://github.com/crypkit/blockapi/commit/240ed21ae5c2ea7bfdc4c23fe4369b58b86d3b05))


## v0.15.0 (2023-02-13)

### Features

- Snx revision
  ([`ee676a1`](https://github.com/crypkit/blockapi/commit/ee676a1e802b969a32ec1ee2083af5a1fb00667a))


## v0.14.10 (2023-02-10)

### Bug Fixes

- Add missing Canto mapping ([#104](https://github.com/crypkit/blockapi/pull/104),
  [`7ef4325`](https://github.com/crypkit/blockapi/commit/7ef43254ce434c894781f8d70a3da5f25c14a286))


## v0.14.9 (2023-02-10)

### Bug Fixes

- Debank keep chain and protocol on coin by symbol
  ([#103](https://github.com/crypkit/blockapi/pull/103),
  [`23aa321`](https://github.com/crypkit/blockapi/commit/23aa3212dcdb21df2c98ed436645fd5c0b1fb9bf))


## v0.14.8 (2023-02-10)

### Bug Fixes

- Add marko requirement
  ([`8a8095f`](https://github.com/crypkit/blockapi/commit/8a8095f9e5ee25c4323701aaae040cdb38bda7b5))

- Add marko requirement
  ([`ec6a57c`](https://github.com/crypkit/blockapi/commit/ec6a57cbaf38392b48047a4965b1ab815a550660))

- Fix optimism snx resolver
  ([`92b4af4`](https://github.com/crypkit/blockapi/commit/92b4af4b0cbbf6d45f3d6fddc635764fd71eeb4e))

- Fix snx optimism contract resolver test
  ([`621f102`](https://github.com/crypkit/blockapi/commit/621f1020ede01166ad198e06884fef11f3149352))

- Fix snx optimism contract resolver test with invalid contract name
  ([`f655c84`](https://github.com/crypkit/blockapi/commit/f655c84fff5e4f9a7ab6840a36672af5ce3bd1f8))

- Fix snx optimism test
  ([`2c28938`](https://github.com/crypkit/blockapi/commit/2c28938ebc41fe8b52d5fa8b23d355ac7b16a392))

- Fix snx optimism test
  ([`a24c5ac`](https://github.com/crypkit/blockapi/commit/a24c5ac3e9197f90064c7d0ea3ab65b48b46e933))

- Freeze vcr
  ([`f5b0e10`](https://github.com/crypkit/blockapi/commit/f5b0e10232e2fb5052c8812e535572236a2a5e99))

- Skip failing test
  ([`abe56af`](https://github.com/crypkit/blockapi/commit/abe56af4022cc72748d061a57ceb9316ee61817c))

- Skip failing test
  ([`b313cb5`](https://github.com/crypkit/blockapi/commit/b313cb5e3840a17763f06950d9df8d238d961747))


## v0.14.7 (2023-02-09)

### Bug Fixes

- Select better coin if contract address is chain
  ([#100](https://github.com/crypkit/blockapi/pull/100),
  [`7b79b8c`](https://github.com/crypkit/blockapi/commit/7b79b8c88ab9d6727d7518c3012f70c4e3146977))

### Chores

- Reformat using new black version ([#101](https://github.com/crypkit/blockapi/pull/101),
  [`c271b48`](https://github.com/crypkit/blockapi/commit/c271b488a309f6cbd948adbf6e61502e049ce72c))


## v0.14.6 (2023-01-31)

### Bug Fixes

- Fix fetching from cosmos api
  ([`a80d3f0`](https://github.com/crypkit/blockapi/commit/a80d3f08f3df89d187e83e44a6d35f33b5f892c5))

- Fix solana contract address and ignore using coingecko ids for cw20 tokens
  ([`9e90d57`](https://github.com/crypkit/blockapi/commit/9e90d57ddcb4c2bd8aa6e27f549a85231b476ff5))


## v0.14.5 (2023-01-11)

### Bug Fixes

- Skip unknown chains when fetching DeBank ([#96](https://github.com/crypkit/blockapi/pull/96),
  [`a75afc5`](https://github.com/crypkit/blockapi/commit/a75afc50fb7ac14bacceb365192a11bbabd1e812))


## v0.14.4 (2023-01-10)

### Bug Fixes

- Fix fetching LUNA
  ([`3b77950`](https://github.com/crypkit/blockapi/commit/3b779506cd6cf4ab0bc14345535019b3de7e208a))


## v0.14.3 (2022-12-20)

### Bug Fixes

- Update coins ([#90](https://github.com/crypkit/blockapi/pull/90),
  [`1667891`](https://github.com/crypkit/blockapi/commit/16678918c702f777f138bd0f8ff98cdb4d59fbcb))


## v0.14.2 (2022-12-16)

### Bug Fixes

- Add tests
  ([`eabe119`](https://github.com/crypkit/blockapi/commit/eabe119ef885ca7196abaf11652e13bb862a045c))

- Fix loading staked amount from subscan
  ([`81f945c`](https://github.com/crypkit/blockapi/commit/81f945c1ef41c7679393ed5d13752b1da1e82629))

- Fix loading staked amount from subscan
  ([`8883059`](https://github.com/crypkit/blockapi/commit/8883059d3147fd5c934ba368e73579133918273f))


## v0.14.1 (2022-12-15)

### Bug Fixes

- Update coingecko mapping ([#87](https://github.com/crypkit/blockapi/pull/87),
  [`06c8810`](https://github.com/crypkit/blockapi/commit/06c8810ba003b3b0be1f0a5219908fb645a26e33))


## v0.14.0 (2022-12-15)

### Features

- Temporary ignore Solana NFTs (or unknown tokens)
  ([`b7fa209`](https://github.com/crypkit/blockapi/commit/b7fa20914634bc283cd544c074123b62d3785a98))


## v0.13.0 (2022-12-15)

### Features

- Add method get_unspent to ChainSoAPI ([#81](https://github.com/crypkit/blockapi/pull/81),
  [`87516c6`](https://github.com/crypkit/blockapi/commit/87516c64b81b00a69808907e2e4bea6944ceb33f))

* Add method get_unspent to ChainSoAPI

* Fix black


## v0.12.0 (2022-12-07)

### Features

- Add Blockchair LTC fetching ([#66](https://github.com/crypkit/blockapi/pull/66),
  [`04dfc8f`](https://github.com/crypkit/blockapi/commit/04dfc8fa5af41619272f3f0db215d805704d9a72))


## v0.11.0 (2022-12-07)

### Features

- Add blockchainos ([#64](https://github.com/crypkit/blockapi/pull/64),
  [`ad39c83`](https://github.com/crypkit/blockapi/commit/ad39c8393df9e8bce177f4f6f1b10ad2ce62ba9b))


## v0.10.0 (2022-12-01)

### Features

- Extend Blockchain Mapping ([#86](https://github.com/crypkit/blockapi/pull/86),
  [`8447b68`](https://github.com/crypkit/blockapi/commit/8447b680bb069f9653f2c3ff232956f1b262fbb4))


## v0.9.0 (2022-11-30)

### Features

- Add kusama support
  ([`d7e8380`](https://github.com/crypkit/blockapi/commit/d7e8380a7d6edf79d71430c52a94a2f8f757fd26))


## v0.8.1 (2022-11-30)

### Bug Fixes

- Make tests less change resisting ([#85](https://github.com/crypkit/blockapi/pull/85),
  [`55091b7`](https://github.com/crypkit/blockapi/commit/55091b7c4f31c3ed3faad0075c0859e03db60fa4))


## v0.8.0 (2022-11-29)

### Features

- Add Blockchair DOGE fetching ([#68](https://github.com/crypkit/blockapi/pull/68),
  [`fd009ea`](https://github.com/crypkit/blockapi/commit/fd009ea193b8984b60edf32186455201abc3497b))


## v0.7.0 (2022-11-16)

### Chores

- Make action skip when there is no release ([#83](https://github.com/crypkit/blockapi/pull/83),
  [`4de25c2`](https://github.com/crypkit/blockapi/commit/4de25c283f4174ada0c26e3865ee6cd5c3b566e4))

- Upgrade actions ([#80](https://github.com/crypkit/blockapi/pull/80),
  [`d62d7db`](https://github.com/crypkit/blockapi/commit/d62d7db78afc8d83128bac12a88dd7b01661168e))

### Features

- Blockchain mapping ([#82](https://github.com/crypkit/blockapi/pull/82),
  [`f84824f`](https://github.com/crypkit/blockapi/commit/f84824f2f496c660861dfc3c133b8ec3af5ca7ca))


## v0.6.0 (2022-11-08)

### Features

- Customize API endpoints ([#79](https://github.com/crypkit/blockapi/pull/79),
  [`7f98c32`](https://github.com/crypkit/blockapi/commit/7f98c327fce5231576b685fea1b5d7596309abdc))


## v0.5.0 (2022-11-01)

### Features

- Add Blockchair BTC fetching ([#65](https://github.com/crypkit/blockapi/pull/65),
  [`c6c00fc`](https://github.com/crypkit/blockapi/commit/c6c00fce934115f6f8323a4e42cbb9738ff15d8b))


## v0.4.2 (2022-10-26)

### Bug Fixes

- Tests and repr implementation ([#76](https://github.com/crypkit/blockapi/pull/76),
  [`cd746f1`](https://github.com/crypkit/blockapi/commit/cd746f1c716204d62e6b0480fca73d3a90afeae3))


## v0.4.1 (2022-10-26)

### Bug Fixes

- **api**: Simplify Synthetix and Perpetual imports
  ([#75](https://github.com/crypkit/blockapi/pull/75),
  [`e1e17e3`](https://github.com/crypkit/blockapi/commit/e1e17e39d99d07bd344d4f9995e65bb9c168ab7e))

### Chores

- Verify PR message ([#74](https://github.com/crypkit/blockapi/pull/74),
  [`87df219`](https://github.com/crypkit/blockapi/commit/87df21920544aaf43c5fa9b256b26ce43d0f8bb7))


## v0.4.0 (2022-10-11)

### Bug Fixes

- Add Synthetix coin ([#72](https://github.com/crypkit/blockapi/pull/72),
  [`fd75722`](https://github.com/crypkit/blockapi/commit/fd757225b6af0baf22ebd1fca309cc7887783d3c))

- Cleanup Coin definitions ([#67](https://github.com/crypkit/blockapi/pull/67),
  [`280b83b`](https://github.com/crypkit/blockapi/commit/280b83bb1b537b3064687ceda79bae99700d0adf))

### Features

- Customize API base URL ([#73](https://github.com/crypkit/blockapi/pull/73),
  [`5db6ba5`](https://github.com/crypkit/blockapi/commit/5db6ba5d57c09af982f0af47211a2d88476c1759))

Co-authored-by: galvanizze <marek.galvanek@gmail.com>


## v0.3.0 (2022-10-07)

### Features

- Add Synthetix fetching ([#63](https://github.com/crypkit/blockapi/pull/63),
  [`4f336ab`](https://github.com/crypkit/blockapi/commit/4f336ab300138eb7a9315d3e13c7516160481a59))


## v0.2.0 (2022-10-06)

### Features

- **ci**: Add GitHub actions ([#61](https://github.com/crypkit/blockapi/pull/61),
  [`2581d8b`](https://github.com/crypkit/blockapi/commit/2581d8b67a47f15f7f3b3c653c4fe1f5d41aa4c3))


## v0.1.23 (2022-09-23)

### Bug Fixes

- `make_checksum_address` returns `None` if `ValueError`
  ([`53a166f`](https://github.com/crypkit/blockapi/commit/53a166f18db2f5562857ada9e853e4c0f2d22cc2))

- Amberdata - ignore tokens when decimals = 0
  ([`69b1cdf`](https://github.com/crypkit/blockapi/commit/69b1cdfee0019bd48876ad0a83d5f950263ea902))

- Changed CHAIN_ID and api_options to abstract properties, removed chain_id from the constructor.
  ([`5a93303`](https://github.com/crypkit/blockapi/commit/5a93303502a8ce45b852dd15335e7bf03a171a91))

- Eth and ethplorer
  ([`c481044`](https://github.com/crypkit/blockapi/commit/c481044675adab93a579bf3dd168048363f4c077))

- Fix eth address
  ([`3ff1e0f`](https://github.com/crypkit/blockapi/commit/3ff1e0f293c309c65513217a9ce7a6bd0c45515e))

- Fixed blochains in covalent api, added missing blockchains.
  ([`5d8cce7`](https://github.com/crypkit/blockapi/commit/5d8cce7485b602235376612a1cece7258bee5d97))

- Return only non-zero solana balances
  ([`a5291ab`](https://github.com/crypkit/blockapi/commit/a5291ab46625035cb03ff9e7831977c54576229f))

- Solana: group by coin address (coins with tags set are not hashable)
  ([`da6dac1`](https://github.com/crypkit/blockapi/commit/da6dac16d8e0d331cf34b1213ffe3fcfad78229a))

- Solana: tried to make it readable
  ([`6a8360b`](https://github.com/crypkit/blockapi/commit/6a8360b191ea37651febcbcc12ece496d17782d4))

- Solana: use of reduceby
  ([`6864440`](https://github.com/crypkit/blockapi/commit/68644400a82bfc7b51a808b6f2c4725e7abefa73))

- **amberdata**: Fix get_balances
  ([`a100f7e`](https://github.com/crypkit/blockapi/commit/a100f7e054f5d3e46647ad5f44668c75c4d6e9af))

- **debank**: Actually get protocol from fetched data
  ([#40](https://github.com/crypkit/blockapi/pull/40),
  [`3f26b5b`](https://github.com/crypkit/blockapi/commit/3f26b5b198cf1a15239f1f1dd7fff0e4869f1d31))

- **debank**: Bnb decimals ([#57](https://github.com/crypkit/blockapi/pull/57),
  [`af1c66e`](https://github.com/crypkit/blockapi/commit/af1c66ef68435f227bedc7b7e07aadb35f7d7eb8))

- **debank**: Fix debank fetching ([#43](https://github.com/crypkit/blockapi/pull/43),
  [`fecec0f`](https://github.com/crypkit/blockapi/commit/fecec0ff57a7c354d2b7a17a3a26fa3b1a4b369b))

* fix(debank): Fix fetching from debank

* fix(debank): less strict getting of tokenset

- **debank**: Update API endpoints ([#58](https://github.com/crypkit/blockapi/pull/58),
  [`eb169ac`](https://github.com/crypkit/blockapi/commit/eb169ace1c5b901539d043d7262891480d8ebe78))

- **ethplorer**: Add default symbol and name in case they're missing
  ([`041376a`](https://github.com/crypkit/blockapi/commit/041376a7ad8c78c1733a81521b9aa1c22cb802c2))

- **terra**: Fix symbols mapping and converting amounts
  ([`247a9f0`](https://github.com/crypkit/blockapi/commit/247a9f0646efde12b68511f25086a0747dd6bcb8))

- **v2**: Unify enums - AssetTypes ([#37](https://github.com/crypkit/blockapi/pull/37),
  [`b198918`](https://github.com/crypkit/blockapi/commit/b19891839dbb9ae7b11d20e951dfc6cdda2a64ee))

### Features

- Add terra money + refactoring
  ([`784c3d2`](https://github.com/crypkit/blockapi/commit/784c3d29cc8e1d2b16cf44a52c7143fa660867b0))

- Add undelegated staked balance and parse staking rewards for each token
  ([#33](https://github.com/crypkit/blockapi/pull/33),
  [`439aad8`](https://github.com/crypkit/blockapi/commit/439aad8a91c286228b9b30491319ce771656026a))

* feat: add undelegated staked balance and parse staking rewards for each token

* fix: replace list comprehension by for cycle

- Added coins to covalenth api objects.
  ([`efd908d`](https://github.com/crypkit/blockapi/commit/efd908d587c0573ca3cd1ead610873dc4767d6f9))

- Added covalenth API base + EthCovalentApi.
  ([`80f3bec`](https://github.com/crypkit/blockapi/commit/80f3bec15eac8fdf24be059f92d749befcd0d83e))

- Added covalenth e2e test
  ([`973352a`](https://github.com/crypkit/blockapi/commit/973352ae9a505459e1c5ee31f3c4c7b4405c6068))

- Added Optimism Ethereum API source.
  ([`155ace5`](https://github.com/crypkit/blockapi/commit/155ace5b584ef43f3bfcf25e05f481839c289c9a))

- Added other blockchains to covalenthq API.
  ([`ee21e7e`](https://github.com/crypkit/blockapi/commit/ee21e7e35d0d7a89678c481553dd6689a1808642))

- Added polygon covalenth api + added implementing of IBalance interface to CovalentApiBase.
  ([`7f10e1e`](https://github.com/crypkit/blockapi/commit/7f10e1e6ca0647d0791c7da7cc3e925417aebe0d))

- Bump blockapi version to `0.1.11`.
  ([`a526644`](https://github.com/crypkit/blockapi/commit/a526644f8029afeddf4dd1278f71c9a9a43a91f7))

- Bump version to 0.1.12.
  ([`c285b3f`](https://github.com/crypkit/blockapi/commit/c285b3f748cafb6a1f4998cd279a6ff571cab5ec))

- Bump version to 0.1.14.
  ([`7a6f31e`](https://github.com/crypkit/blockapi/commit/7a6f31e3186b22bfe23b301ac9f73cf9425263e1))

- Bump version to 0.1.4
  ([`145a1fc`](https://github.com/crypkit/blockapi/commit/145a1fc3ea1750a464547acd859dcb3a75557789))

- Fetch ibc data for terra tokens
  ([`697ab8e`](https://github.com/crypkit/blockapi/commit/697ab8e3998717f0120eb27010127c990af4da8f))

- Fix solana fetching
  ([`99dd481`](https://github.com/crypkit/blockapi/commit/99dd481e269eca807a341a8a009a9e63900725de))

- Increase version
  ([`0d45050`](https://github.com/crypkit/blockapi/commit/0d4505050b56aa7ea0d5eb812d5e14e9b3c44570))

- Introducing v2 - basic objects + ethplorer
  ([`e7e5904`](https://github.com/crypkit/blockapi/commit/e7e59049bf10843878ad19c5731f415488e59492))

- Merged covalent e2e tests into general test, refactoring.
  ([`6e17db5`](https://github.com/crypkit/blockapi/commit/6e17db5c52591b7dd79b3281ccaa9ad14bf6be80))

- Moved rate limit to base class, removed coin class attr.
  ([`5ec58ef`](https://github.com/crypkit/blockapi/commit/5ec58ef70c349ba0252bcf9fa07dd06193277dad))

- Refactoring + add terra api with 2 sources
  ([`4a8a644`](https://github.com/crypkit/blockapi/commit/4a8a644959f0faf6d06cab0d971aa42d1fd14de9))

- Removed address param from constructor, moved directly to the get_balance method.
  ([`244146b`](https://github.com/crypkit/blockapi/commit/244146b54474815cdc3cb6fec94852147a6666d3))

- Solana: token accounts with the same coin merged into one.
  ([`ecdacbb`](https://github.com/crypkit/blockapi/commit/ecdacbbebf86c64c24da7c24c483cb1941f9e187))

- Solana: token accounts with the same coin merged into one.
  ([`13362ff`](https://github.com/crypkit/blockapi/commit/13362ff140b7a35b6f42669856293f4f05784fdb))

- V2 reformatting using isort and black
  ([`542e0ad`](https://github.com/crypkit/blockapi/commit/542e0ad855142a10859cec95b7dfeb35bc60ebcf))

- **alethio**: Rename contract address field in get_balance
  ([`64335e3`](https://github.com/crypkit/blockapi/commit/64335e30392617fba5f7be5b8a521fec67dd9f4e))

- **amberdata**: Add AmberData API for ETH
  ([`edde498`](https://github.com/crypkit/blockapi/commit/edde4981987716983af7568ab7392f5d6ea44c65))

- **api**: Kyber Network support ([#22](https://github.com/crypkit/blockapi/pull/22),
  [`c886cef`](https://github.com/crypkit/blockapi/commit/c886cef954a504fc926c132b30acddc71abe5f12))

- **api**: New api TzStats implementation
  ([`af41839`](https://github.com/crypkit/blockapi/commit/af418392ff932d102f7177c79775262d9e20baac))

- **api + test**: (#19)
  ([`956bdf6`](https://github.com/crypkit/blockapi/commit/956bdf6282b457624adc190601dfcef6e7fcee02))

- on_failure_return_none removed - several typo and style fixes - several functional fixes - tests
  for several providers (motivated by Crypkit use-cases so not all providers and not all subclasses
  were tested)

- **debank**: Add configuration for is_all ([#53](https://github.com/crypkit/blockapi/pull/53),
  [`56a1e36`](https://github.com/crypkit/blockapi/commit/56a1e364651e8dbf97dc50d2c89ac4f3aef55f93))

* feat(debank): Add configuration for is_all

* chore(blockapi): Update version

* fix(debank): Don't convert bool to string

- **debank**: Add is_wallet flag ([#39](https://github.com/crypkit/blockapi/pull/39),
  [`4fbb212`](https://github.com/crypkit/blockapi/commit/4fbb212027d5b24d8e1789ed364fe6343e022fb3))

* feat(debank): Add is_wallet flag

* feat(debank): Update version to 0.1.10

- **debank**: Add native Coin mapping
  ([`75bf360`](https://github.com/crypkit/blockapi/commit/75bf36013e2aa2656a9ca1dcdc8b23e361e2ec25))

* feat(debank): Add coin mapping

* fix(debank): Update token name

* Remove unnecessary log message

* Update package version

- **debank**: Add token_use ([#54](https://github.com/crypkit/blockapi/pull/54),
  [`89dc284`](https://github.com/crypkit/blockapi/commit/89dc2849c80f9cd4e599e46f2b01f43e09f98a90))

* feat(debank): Add token_use

* feat(debank): Add pool_id to BalanceItem

* Rename TokenUse -> TokenRole

* Add LiquidityPool token role

- **debank**: Properly convert protocol chain ([#59](https://github.com/crypkit/blockapi/pull/59),
  [`feea912`](https://github.com/crypkit/blockapi/commit/feea91244a2198b8975f3e983eb731d2c6676d84))

- **debank**: Use pro API. Add keys. ([#56](https://github.com/crypkit/blockapi/pull/56),
  [`1de8c81`](https://github.com/crypkit/blockapi/commit/1de8c814c2bed0547364d5bf6b238d99be41dc95))

* feat(debank): Use pro API. Add keys

* Change dummy key to be more explicit

* feat(debank): Enable proxy

- **debank**: Use pydantic model to verify data structure
  ([#51](https://github.com/crypkit/blockapi/pull/51),
  [`b27cdba`](https://github.com/crypkit/blockapi/commit/b27cdba0988abb6902ffad4f4e2ddead279d4c05))

* feat(debank): Use pydantic model to verify data structure

* Fix type hint and method name

* Improve log message

* Add pydantic dependency

- **eth_apis**: Update eth apis rate limits
  ([`4f44f9c`](https://github.com/crypkit/blockapi/commit/4f44f9cb0649ac81da6909609dfd4c8bc66904b1))

- **Perpetual**: Add Perpetual fetching ([#38](https://github.com/crypkit/blockapi/pull/38),
  [`7c9ed26`](https://github.com/crypkit/blockapi/commit/7c9ed26c13718f8746e647114ede92f22b707943))

* feat(Perpetual): Add Perpetual fetching

* feat(Perpetual): Fix blockchain settings

- **release**: New release
  ([`a207bd9`](https://github.com/crypkit/blockapi/commit/a207bd9a152da85150f44def89714378fb1dc66b))

- **release**: New release
  ([`3d86d60`](https://github.com/crypkit/blockapi/commit/3d86d60bdce0fa1dc6f926e38b453f605650cbc1))

- **release**: New release 0.0.72
  ([`6e990ad`](https://github.com/crypkit/blockapi/commit/6e990ad8cd3cc8a5963ac39fd90c34a555d02d2b))

- **release**: New release 0.0.74
  ([`7bf5774`](https://github.com/crypkit/blockapi/commit/7bf577433c4cdcfac1a853074ee7c13e80fddd82))

- **request**: Don't use basic rate limiter by default
  ([`2d7420d`](https://github.com/crypkit/blockapi/commit/2d7420d6e4556a96804f593a0b42b6fca5118117))

- **requirements**: Delete unused gevent package
  ([`2725dbb`](https://github.com/crypkit/blockapi/commit/2725dbbac4e6fc2950ee2885597a35abbf63b16a))

- **terra**: Terra money implementation
  ([`3512eef`](https://github.com/crypkit/blockapi/commit/3512eef4e3e0e4c4eb2a525f06a0c686322f84a3))

- **test**: Add providers testing and diagnostic class + fix on RVN
  ([#24](https://github.com/crypkit/blockapi/pull/24),
  [`d08b8b9`](https://github.com/crypkit/blockapi/commit/d08b8b96f71df08af1fac04a97912d58d568c733))

- **test**: Decred tests + minor fixes on decred
  ([#14](https://github.com/crypkit/blockapi/pull/14),
  [`1d2a0c8`](https://github.com/crypkit/blockapi/commit/1d2a0c8c8e96a70daa18709c8ab948137bdfe99e))

- **test**: Tezos tests + minor fixes on tezos + new xtz explorer added
  ([#15](https://github.com/crypkit/blockapi/pull/15),
  [`ef9ecfa`](https://github.com/crypkit/blockapi/commit/ef9ecfa0f2a480268d38b6d3c88aeb37b1c30867))

* feat(test): tezos tests + minor fixes on tezos + new xtz explorer added

* feat(test): decred tests + minor fixes on decred (#14)

* fix(api): cosmos balance + test fixes

* fix(api): api_key argument added

- **version**: Increase version
  ([`7e2bdcf`](https://github.com/crypkit/blockapi/commit/7e2bdcf72f576d88ecbcc748f8c5d5cbe1a23bba))

### Refactoring

- **api**: Overflows cosmetic changes + cosmos functional fixes +
  ([#13](https://github.com/crypkit/blockapi/pull/13),
  [`71162f3`](https://github.com/crypkit/blockapi/commit/71162f33af011cee1f6eb3eb3513cbaf034fffeb))

pytest implemented
