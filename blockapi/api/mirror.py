from decimal import Decimal

from blockapi.services import BlockchainAPI


class MirrorApi(BlockchainAPI):


    symbol = 'LP'
    base_url = 'https://tequila-lcd.terra.dev'
    rate_limit = 0.5
    coef = Decimal(1e-6)
    max_items_per_page = 100
    page_offset_step = 1

    supported_requests = {
        'get_mirror_pool_balance':  '/wasm/contracts/{lp_token_contract}/store' 
                                    '?query_msg={{ "balance" : {{  "address" : "{address}" }} }}',
        'get_mirror_pool':          '/wasm/contracts/{pair_contract}/store'
                                    '?query_msg={{ "pool": {{ }} }}'
    }

    symbols = {
        'uluna': 'LUNA',
        'ukrw': 'KRT',
        'usdr': 'SDT',
        'uusd': 'UST',
        'umnt': 'MNT'
    }

    liqudity_pool_suffix = "LP"


    def get_balance(self):
        return ""

    def get_contracts(self):
        # Make a mechanism to fetch the contracts by the initialization of the api or a mechanism to get this from DB for translation of contract address to ticker
        terra_contracts = {
            "contracts": {
                "gov": "terra12r5ghc6ppewcdcs3hkewrz24ey6xl7mmpk478s",
                "mirrorToken": "terra10llyp6v3j3her8u3ce66ragytu45kcmd9asj3u",
                "factory": "terra10l9xc9eyrpxd5tqjgy6uxrw7dd9cv897cw8wdr",
                "oracle": "terra1uvxhec74deupp47enh7z5pk55f3cvcz8nj4ww9",
                "mint": "terra1s9ehcjv0dqj2gsl72xrpp0ga5fql7fj7y3kq3w",
                "staking": "terra1a06dgl27rhujjphsn4drl242ufws267qxypptx",
                "tokenFactory": "terra18qpjm4zkvqnpjpw0zn0tdr8gdzvt8au35v45xf",
                "collector": "terra1v046ktavwzlyct5gh8ls767fh7hc4gxc95grxy",
                "community": "terra10qm80sfht0zhh3gaeej7sd4f92tswc44fn000q",
                "airdrop": "terra1p6nvyw7vz3fgpy4nyh3q3vc09e65sr97ejxn2p"
            },
            "whitelist": {
                "terra10llyp6v3j3her8u3ce66ragytu45kcmd9asj3u": {
                    "symbol": "MIR",
                    "name": "Mirror",
                    "token": "terra10llyp6v3j3her8u3ce66ragytu45kcmd9asj3u",
                    "pair": "terra1cz6qp8lfwht83fh9xm9n94kj04qc35ulga5dl0",
                    "lpToken": "terra1zrryfhlrpg49quz37u90ck6f396l4xdjs5s08j",
                    "status": "LISTED"
                },
                "terra16vfxm98rxlc8erj4g0sj5932dvylgmdufnugk0": {
                    "symbol": "mAAPL",
                    "name": "Apple",
                    "token": "terra16vfxm98rxlc8erj4g0sj5932dvylgmdufnugk0",
                    "pair": "terra1yj892rl8edvk0y2ayf3h36t6uf89lzxg8jea4a",
                    "lpToken": "terra1vth958fsn8zawllaqcdzswksjkv3dz2sqqmcu4",
                    "status": "LISTED"
                },
                "terra1qg9ugndl25567u03jrr79xur2yk9d632fke3h2": {
                    "symbol": "mGOOGL",
                    "name": "Google",
                    "token": "terra1qg9ugndl25567u03jrr79xur2yk9d632fke3h2",
                    "pair": "terra1z2734asgwhma8ma2fq4yu7ce2l3mrvj4qnz6ws",
                    "lpToken": "terra1qxurxcgl30eu4ar34ltr5e9tqc2gjl4atspvy3",
                    "status": "LISTED"
                },
                "terra1nslem9lgwx53rvgqwd8hgq7pepsry6yr3wsen4": {
                    "symbol": "mTSLA",
                    "name": "Tesla",
                    "token": "terra1nslem9lgwx53rvgqwd8hgq7pepsry6yr3wsen4",
                    "pair": "terra1tsln42kfeq8edwscmw8njgter5dp8evn40znn9",
                    "lpToken": "terra1utf7qw0uce42vqsh255hxgd3pvuzfvp6jcayk5",
                    "status": "LISTED"
                },
                "terra1djnlav60utj06kk9dl7defsv8xql5qpryzvm3h": {
                    "symbol": "mNFLX",
                    "name": "Netflix",
                    "token": "terra1djnlav60utj06kk9dl7defsv8xql5qpryzvm3h",
                    "pair": "terra18yl0z6wntjkustt9cckc9ptp7l5qh7kr0xrmav",
                    "lpToken": "terra1e0njrqcsehxpt9due62x9zsxl7h9htl0xqdujv",
                    "status": "LISTED"
                },
                "terra18yx7ff8knc98p07pdkhm3u36wufaeacv47fuha": {
                    "symbol": "mQQQ",
                    "name": "Invesco QQQ Trust",
                    "token": "terra18yx7ff8knc98p07pdkhm3u36wufaeacv47fuha",
                    "pair": "terra1epxv8z6tzxezjfgw7tveytw5n3fuf6wvg6w8f5",
                    "lpToken": "terra1h52zc9qmndczgru9vp2cvuwfclyykl5yt3qjk8",
                    "status": "LISTED"
                },
                "terra1ax7mhqahj6vcqnnl675nqq2g9wghzuecy923vy": {
                    "symbol": "mTWTR",
                    "name": "Twitter",
                    "token": "terra1ax7mhqahj6vcqnnl675nqq2g9wghzuecy923vy",
                    "pair": "terra1jv937296dy5c5dxglrzf05h0jlaaxp55tqlyh6",
                    "lpToken": "terra10cugucjwn4hdtvavl0n2sh2ke64nx93luhj49k",
                    "status": "LISTED"
                },
                "terra12s2h8vlztjwu440khpc0063p34vm7nhu25w4p9": {
                    "symbol": "mMSFT",
                    "name": "Microsoft Corporation",
                    "token": "terra12s2h8vlztjwu440khpc0063p34vm7nhu25w4p9",
                    "pair": "terra1dt7ne6gwv23wg6chl89q95yj6999alagc6rqd9",
                    "lpToken": "terra1f7azmktepw5rq35e2m6r6smtwl8wdrxp0dsvar",
                    "status": "LISTED"
                },
                "terra12saaecsqwxj04fn0jsv4jmdyp6gylptf5tksge": {
                    "symbol": "mAMZN",
                    "name": "Amazon.com",
                    "token": "terra12saaecsqwxj04fn0jsv4jmdyp6gylptf5tksge",
                    "pair": "terra1xs3vy9zs8agmnzyn7z9s7kqk392uu2h3x3l6er",
                    "lpToken": "terra1kgvcrtupc8y4dgc9n08ud99ckdxp08j59zgccf",
                    "status": "LISTED"
                },
                "terra15dr4ah3kha68kam7a907pje9w6z2lpjpnrkd06": {
                    "symbol": "mBABA",
                    "name": "Alibaba Group Holdings Ltd ADR",
                    "token": "terra15dr4ah3kha68kam7a907pje9w6z2lpjpnrkd06",
                    "pair": "terra15qq59h2canrr2pf8ny7rw57nx3mcvw97tp3xj4",
                    "lpToken": "terra1px2ya3e07aprfgc76e57r3nuvy3czssrvcxg9t",
                    "status": "LISTED"
                },
                "terra19dl29dpykvzej8rg86mjqg8h63s9cqvkknpclr": {
                    "symbol": "mIAU",
                    "name": "iShares Gold Trust",
                    "token": "terra19dl29dpykvzej8rg86mjqg8h63s9cqvkknpclr",
                    "pair": "terra1tq6w7rl4ryrk458k57dstelx54eylph5zwnpf9",
                    "lpToken": "terra193c2xvuzswct8qtsg4e6qhe3hyt3l6fac9cy79",
                    "status": "LISTED"
                },
                "terra1fdkfhgk433tar72t4edh6p6y9rmjulzc83ljuw": {
                    "symbol": "mSLV",
                    "name": "iShares Silver Trust",
                    "token": "terra1fdkfhgk433tar72t4edh6p6y9rmjulzc83ljuw",
                    "pair": "terra1tyzsl0dw4pltlqey5v6g646hm22pql8vy3yh2g",
                    "lpToken": "terra16cn5cgwaktrzczda0c6ux0e2quudh4vn3t8jjm",
                    "status": "LISTED"
                },
                "terra1fucmfp8x4mpzsydjaxyv26hrkdg4vpdzdvf647": {
                    "symbol": "mUSO",
                    "name": "United States Oil Fund, LP",
                    "token": "terra1fucmfp8x4mpzsydjaxyv26hrkdg4vpdzdvf647",
                    "pair": "terra1llk7ycwwlj2zs2l2dvnvmsxrsrnucqwaltstcf",
                    "lpToken": "terra1rag9w5ch0jrdxjffr6napqz0zsrpm6uz2zezmj",
                    "status": "LISTED"
                },
                "terra1z0k7nx0vl85hwpv3e3hu2cyfkwq07fl7nqchvd": {
                    "symbol": "mVIXY",
                    "name": "ProShares VIX",
                    "token": "terra1z0k7nx0vl85hwpv3e3hu2cyfkwq07fl7nqchvd",
                    "pair": "terra1xg2393l4s7n4z2r0cnu4rr55mkpp942f4d3qzr",
                    "lpToken": "terra1ud750vcv39hd467sj2kk6s6nn8zf5xhgggf7uq",
                    "status": "LISTED"
                }
            }
        }
        pool_contracts = terra_contracts['whitelist']
        return pool_contracts


    def get_pool_lp_balance(self, lp_token_contract):
        """Gets a balance denominated in LPs based on the "lpToken" contract address from whitelist

        :param lp_token_contract: Contract of the lp token from whitelist on the running network (ex. terra1zrryfhlrpg49quz37u90ck6f396l4xdjs5s08j)
        :type lp_token_contract: str
        :returns: A string with the LP balance
        :rtype: str
        """
        response = self.request('get_mirror_pool_balance',  lp_token_contract=lp_token_contract, address=self.address)

        # if possible check if the returned ballance is for the right contract (different query) and throw exception in case response doesn't have the right format
        balance = response['result']['balance']
        return balance



    def get_pool_info(self, pair_contract):
        """Gets pool information from a the paircontract from the whitelist

        :param pair_contract: Contract adress of the pair (ex. terra1cz6qp8lfwht83fh9xm9n94kj04qc35ulga5dl0)
        :type pair_contract: str
        :returns: A json dict with details of the pool (ex. {'stablecoin_amount': '552499703522', 'stablecoin_symbol': 'UST', 'token_amount': '1323959908110', 'token_symbol': 'MIR', 'total_share': '851877273095'})
        :rtype: dict
        """

        response = self.request('get_mirror_pool', pair_contract=pair_contract, address=self.address)

        # Rewrite this one to check if the asset No. 0 is really usd in case there will be more fiat pegged currencies in Mirror or in case the order of assets will be different
        stablecoin_amount = response['result']['assets'][0]['amount'];
        stablecoin_symbol = response['result']['assets'][0]['info']['native_token']['denom'];
        stablecoin_symbol = self._get_symbol(stablecoin_symbol)

        # Rewrite this one to be sure we really get the token amount an of the right token
        token_amount = response['result']['assets'][1]['amount'];
        token_contract = response['result']['assets'][1]['info']['token']['contract_addr'];
        token_symbol = self.get_token_symbol(token_contract)
        total_share = response['result']['total_share']

        # Maybe pass this as python object with attributes instead of loose type:dict
        pool_info = {
            'stablecoin_amount' : stablecoin_amount,
            'stablecoin_symbol' : stablecoin_symbol,
            'token_amount' : token_amount,
            'token_symbol' : token_symbol,
            'total_share' : total_share
        }

        return pool_info


    def get_token_symbol(self , contract_addr):
        """Gets and returns a token symbol form the speficied token contractaddress

        :param contract_addr: Contract of the token from whitelist on the running network (ex. terra10llyp6v3j3her8u3ce66ragytu45kcmd9asj3u)
        :type contract_addr: str
        :returns: A string with the symbol (ex. UUSD)
        :rtype: str
        """

        contracts = self.get_contracts()
        symbol = contract_addr

        for contract in contracts:
            if (contracts[contract]['token'] == contract_addr):
                symbol = contracts[contract]['symbol']

        if (symbol == contract_addr):
            ex = Exception('Could not get symbol based on token address! Check the local copy of whitelisted contracts if it is up to date!')
            raise ex

        return symbol



    def fetch_pool_balances(self):
        """Fetches all pool balances connected to the wallet provided in intialization of the api class

        :returns: A json dict with pool balances and withdrawable assets ballances (ex. of one pool balance [{'symbol': 'MIR-UST LP', 'amount': '71.152144', 'underlying_assets': [{'symbol': 'MIR', 'amount': '110.582344'}, {'symbol': 'UST', 'amount': '46.146951'}]}, { ... } ] )
        :rtype: dict
        """

        contracts = self.get_contracts()
        response = []

        # loop through the pool contracts and construct the response
        # that consist of pool balances of individual pools
        for contract in contracts:
            lp_contract = contracts[contract]['lpToken']
            lp_balance = self.get_pool_lp_balance(lp_contract)


            if ( Decimal(lp_balance) > 0 ):

                symbol = contracts[contract]['symbol']
                #print("LP ballance biiger than zero for : " + symbol)

                token_contract = contracts[contract]['token']
                pair_contract = contracts[contract]['pair']
                pool_info = self.get_pool_info(pair_contract)

                lp_balance_decimal = Decimal(lp_balance) * self.coef
                withdrawable_stablecoin =  Decimal(pool_info['stablecoin_amount']) / Decimal(pool_info['total_share']) * lp_balance_decimal
                withdrawable_token = Decimal(pool_info['token_amount']) / Decimal(pool_info['total_share']) * lp_balance_decimal

                pool_symbol = symbol + '-' + pool_info['stablecoin_symbol'] + ' ' + self.liqudity_pool_suffix

                pool_fragment =  {
                    'symbol' : pool_symbol,
                    'amount' : format( lp_balance_decimal , '.6f'),
                    'underlying_assets' : [
                        {
                            'symbol': pool_info['token_symbol'],
                            'amount': format( withdrawable_token , '.6f'),
                        },
                        {
                            'symbol': pool_info['stablecoin_symbol'],
                            'amount' : format( withdrawable_stablecoin , '.6f'),
                        }
                    ]
                }

                response.append(pool_fragment)
                #print(response)

        return response

    @classmethod
    def _get_symbol(cls, denom):
        """It seems that API returns only denom instead of correct
        symbols.
        """
        return cls.symbols.get(denom, 'unknown')