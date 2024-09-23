import logging
import os

HTTP_PROXY_URL = 'http://127.0.0.1:7890'
#HTTP_PROXY_URL = 'http://127.0.0.1:8234'
#HTTP_PROXY_URL = None

LOG_LEVEL = logging.DEBUG

env_dist = os.environ

DATA_PATH = env_dist.get('DATA_PATH') if env_dist.get('DATA_PATH') else "/Users/adam/Code/swapbot/data/"
LOG_PATH = env_dist.get('LOG_PATH') if env_dist.get('LOG_PATH') else f"/tmp/"

# 主流币定义： 和稳定币的交易对LP/2达到100万刀
MAIN_COIN_LIQT = 1000000
# 有价值的币定义： 和稳定币/主流币的LP/2达到5万刀
VALUEABLE_COIN_LIQT = 5000

MIN_ARBI_AMOUNT = 50

ZEROADDR = '0x0000000000000000000000000000000000000000'

CHAIN_NAME = [
    "eth",
    "heco",
    "hecotest",
    "bsc",
    "bsctest",
    "rinkeby",
    "ropsten",
    "kovan",
    "goerli",
    "ftm",
    'avax',
    'avaxtest',
    'karastar'
]

GAS_PRICE = {
    "kovan": 30,
    'heco': 2,
    'matic': 35,
    "ropsten": 8,
    'bsc': 5.1,
    'bsctest': 20,
    'ftm': 160,
    'eth': 90,
    'avaxtest': 27,
    'avax': 27,
    'rinkeby': 3,
}


CHAIN_ID = {
    "eth": 1,
    "heco": 128,
    "bsc": 56,
    "hecotest": 256,
    "mainnet": 1,
    "ropsten": 3,
    'bsctest': 97,
    "rinkeby": 4,
    "goerli": 5,
    "kovan": 42,
    "matic": 137,
    "ftm": 250,
    'avaxtest': 43113,
    'avax': 43114,
    'karastar': 111
}

NFT_ADDRESS = {
    "rinkeby": {
        'dsg': '0xcc14dd8e6673fee203366115d3f9240b079a4930'
    },
    "eth": {
        'punk_comic': '0x128675d4fddbc4a0d3f8aa777d8ee0fb8b427c2f',
        'pepsi': '0xa67d63e68715dcf9b65e45e5118b5fcd1e554b5f',
        'witch': '0x5180db8f5c931aae63c74266b211f580155ecac8',
        'coder': '0x15de1beb13d7d38cbc493d3ecbc0c7650e715c22',
        'fomodoge': '0x90cfce78f5ed32f9490fd265d16c77a8b5320bd4',
        'shark':'0x4372f4d950d30c6f12c7228ade77d6cc019404c9',
        'zen333': '0xf64e6fb725f04042b5197e2529b84be4a925902c',
        'bayc': '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d',
        'nftwhale': '0xnftwhale',
        'jumpman': '0x495f947276749ce646f68ac8c248420045cb7b5e'
    }
}

CONTRACT_ADDRESS = {
    "rinkeby": {
        'opensea_ex': '0x5206e78b21ce315ce284fb24cf05e0585a93b1d9',
    },
    "avax": {
        'wavax': '0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7',
        'usdt': '0xc7198437980c041c805a1edcba50c1ce5db95118',
        'usdc': '0xa7d7079b0fead91f3e65f86e8915cb59c1a4c664',
        'cra': '0xA32608e873F9DdEF944B24798db69d80Bbb4d1ed',
        'tus': '0xf693248F96Fe03422FEa95aC0aFbBBc4a8FdD172',
        'craft': '0x8aE8be25C23833e0A01Aa200403e826F611f9CD2',
        'bulksender': '0x2EFa196a0972a501b804131A2276E82d60BA7C90',
        'joe_swap': {
            'factory': '0x9ad6c38be94206ca50bb0d90783181662f0cfa10',
            'router': '0x60ae616a2155ee3d9a68541ba4544862310933d4'
        }
    },
    "avaxtest": {

    },
    "eth": {
        'usdt': '0xdac17f958d2ee523a2206206994597c13d831ec7',
        'opensea_ex': '0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b',
        'pop': '0xd0cd466b34a24fcb2f87676278af2005ca8a78c4',
        'weth': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'bulksender': '0xb72Eb25bb962F6177c962cD5cb86EaC4680941eE',
        'uni_swap': {'factory': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
                     'router': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'},
        'go_swap': {'factory': '0x96422EE8256d621B9AE79B90B1eFB8fd8B3FCe11',
                    'router': '0xd184b42c7f8d805DccB23BD986a4A53aB72D43b2'},
        'sushi_swap': {'factory': '0xc0aee478e3658e2610c5f7a4a2e1777ce9e4f2ac',
                       'router': '0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f'},
        'uniswapv3': {
            'factory': '0x1F98431c8aD98523631AE4a59f267346ea31F984',
            'router': '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD',
            'quoter': '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6',
            'universalrouter': '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD'
        }
    },
    "ropsten": {
        'bulksender': '0x4ecE77753D06051E6E77bd3f021A107E88d0B636',
    },
    "bsctest": {
        'wbnb': "0x0a6160c54eF1CEf763e2aC9426013CC4138A7518",
        'kusd': "0xfc8e59a6ed9c61c8231388e0e507a281033fc5dc",
        'usdt': "0x0a6160c54eF1CEf763e2aC9426013CC4138A7518",
        'fupo': "0x0a6160c54eF1CEf763e2aC9426013CC4138A7518",
        'bulksender': '0x7a99075e0f0a9271782e2b44560a1fe79b8b584b',
        'jojo_box_1': '0x7006c3570FAeCC5B498FAC86dA99119F91215fc8',
        'go_swap': {
            'factory': '0xb88040a237f8556cf63e305a06238409b3cae7dc',
            'router': '0xb88040a237f8556cf63e305a06238409b3cae7dc'},
        'pancaketest_swap': {
            'factory': '0xb7926c0430afb07aa7defde6da862ae0bde767bc',
            'router': '0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3'},
    },
    "matic": {

        'gamee': '0xcf32822ff397ef82425153a9dcb726e5ff61dca7',
        'try': '0xefee2de82343be622dcb4e545f75a3b9f50c272d',
        'wmatic': '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270',
        'usdt': '0xc2132d05d31c914a87c6611c10748aeb04b58e8f',
        'usdc': '0x2791bca1f2de4661ed88a30c99a7a9449aa84174',
        'bulksender': '0xb754103ddc5929dd418bf4d6077f329708a229b6',
        'metaswap': '0x1a1ec25DC08e98e5E93F1104B5e5cdD298707d31',
        'paraswap': '0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57',
        'clam': '0x4d6A30EFBE2e9D7A9C143Fce1C5Bb30d9312A465',
        'mai': '0xa3Fa99A148fA48D14Ed51d610c367C61876997F1',
        'kusd': '0x6d43Fcc20c814f141Dd51742399De8ba75B4a95f',  # in b30 address
        'ko': '0x8461e1619a91749d4E04F410ef889F3B0B6982CD',  # in b30 address
        'otter_stake': '0x314de54E2B64E36F4B0c75079C7FB7f894750014',
        'sushi_swap': {
            'factory': '0xc35DADB65012eC5796536bD9864eD8773aBc74C4',
            'router': '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506'
        },
        'quick_swap': {
            'factory': '0x5757371414417b8c6caad45baef941abc7d3ab32',
            'router': '0xa5e0829caced8ffdd4de3c43696c57f7d7a678ff'
        }
    },
    "bsc": {
        # 'num': '0xeceb87cf00dcbf2d4e2880223743ff087a995ad9',
        # 'desu': '0x32f1518baace69e85b9e5ff844ebd617c52573ac',
        # 'porto':'0x49f2145d6366099e13b10fbf80646c0f377ee7f6',
        # 'dot': '0x7083609fce4d1d8dc0c979aab8c869ea2c873402',
        'santos': '0xa64455a4553c9034236734faddaddbb64ace4cc7',
        'raca': '0x043b49749e0016e965600d502e2177ca2d95b3d9',
        # 'raca2': '0x12bb890508c125661e03b09ec06e404bc9289040',
        'bp': '0xacb8f52dc63bb752a51186d1c55868adbffee9c1',
        'baby': '0x53e562b9b7e5e94b81f10e96ee70ad06df3d2657',
        'ada': '0x3ee2200efb3400fabb9aacf31297cbdd1d435d47',
        'busd': '0xe9e7cea3dedca5984780bafc599bd69add087d56',
        'usdc': '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d',
        'usdt': '0x55d398326f99059ff775485246999027b3197955',
        'bulksender': '0xba75ce4219d248d2ce2a6cee5ff4bafeee87bae9',
        'metaswap': '0x1a1ec25DC08e98e5E93F1104B5e5cdD298707d31',
        'eggswap': '0xE9C7650b97712C0Ec958FF270FBF4189fB99C071',
        'dsg': '0x9A78649501BbAAC285Ea4187299471B7ad4ABD35',
        'cake': '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82',
        'vai': '0x4bd17003473389a42daf6a0a729f6fdb328bbbd7',
        'banana': '0x603c7f932ed1fc6575303d8fb018fdcbb0f39a95',
        'wbnb': '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c',
        'oro': '0xFc4f5A4d1452B8Dc6C3CB745dB15B29c00812b19',
        'elemon': '0xE3233fdb23F1c27aB37Bd66A19a1f1762fCf5f3F',
        # 'fake_elemon': '0xc74e0d65ef9e36030ec777098aee57b4d17412f0',
        # 'jojo': '0x78A499a998Bdd5a84CF8b5aBe49100D82DE12f1C',
        # 'jojo_box_1': '0xc33b4cf266ac649538a662bb394c5ac1e6a8702c',  # jojo 盲盒
        # 'jojo_auction': '0x8b0b26b97aa4b907dd8dfe71fd0b602d71bb7df4',
        # 'gfloki': '0x53b3338e3345758ae88b930e3d9759a95c5ce05c',
        # 'aspo': '0x1a9b49e9f075c37fe5f86c916bac9deb33556d7e',
        # 'aspo0': '0x4a72e6b0614a681586eac7b74455865e0e45ba86',
        # 'aspo2': '0xb6309ede8e8db49f1e99251c6a827fa5afacbbce',
        'fupo': '0x445aBdB0294b9967f76DBa722B973Dc03fa244fA',
        'kou': '0xb0ba6978ad395820c1a24a11cc9f28827a26c2f8',
        # 'titan': '0x0c1253a30da9580472064a91946c5ce0C58aCf7f',
        # 'zuki' : '0xE81257d932280AE440B17AFc5f07C8A110D21432',
        # 'spay' : '0x13A637026dF26F846D55ACC52775377717345c06',
        'bsw': '0x965f527d9159dce6288a2219db51fc6eef120dd1',
        'milk': '0xbf37f781473f3b50e82c668352984865eac9853f',
        # 'jok': '0x01681E3a7c86Fc27B0764814051A67f7e02661C1',
        'hro': '0xfb1a34eb2585b0ad7976420d7a21ef2f4aebeeb6',
        'rice': '0x338AF54976B9D4F7F41c97dcb60dFEc0694149f9',
        'htd': '0x5E2689412Fae5c29BD575fbe1d5C1CD1e0622A8f',
        'sea': '0x26193C7fa4354AE49eC53eA2cEBC513dc39A10aa',
        'ape_swap': {
            'factory': '0x0841BD0B734E4F5853f0dD8d7Ea041c241fb0Da6',
            'router': '0xcF0feBd3f17CEf5b47b0cD257aCf6025c5BFf3b7'
        },
        'pancake_swap': {
            'factory': '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73',
            'router': '0x10ED43C718714eb63d5aA57B78B54704E256024E'},
        'dsg_swap': {
            'factory': '0x73D9F93D53505cB8C4c7f952ae42450d9E859D10',
            'router': '0xE9C7650b97712C0Ec958FF270FBF4189fB99C071'},
        'biswap': {
            'factory': '',
            'router': '0x3a6d8ca21d1cf76f653a67577fa0d27453350dd8'
        },
        'arbtrage_1': '',

    },
    'kovan': {
        'weth': '0xd0A1E359811322d97991E03f863a0C30C2cF029C',
        'unikovan_swap': {'factory': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
                          'router': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'},
        'go': {'factory': '0x96422EE8256d621B9AE79B90B1eFB8fd8B3FCe11',
               'router': '0xd184b42c7f8d805DccB23BD986a4A53aB72D43b2'},
        'ko': "0xb495afF44570bBb60505D747aedD9B88645fD9A6",
        'kusd': "0xBD8bC7f37347e6806d0ec3F65C5f16f570b4762A",
        'gokovan_swap': {
            'factory': '0x96422EE8256d621B9AE79B90B1eFB8fd8B3FCe11',
            'router': '0xd184b42c7f8d805DccB23BD986a4A53aB72D43b2'
        },
    },

    'heco': {
        'mdis': {'factory': '0x2F3F03b6a1B1d73b01390E234AE813bc06d5B8e8',
                 'router': '0x40367258BB8b9195446E99079391D7Ccb5AaeaB9'},
        'bxh': {'factory': '0xe0367ec2bd4Ba22B1593E4fEFcB91D29DE6C512a',
                'router': '0x00eFB96dBFE641246E961b472C0C3fC472f6a694'},
        'mdex': {'factory': '0xb0b670fc1F7724119963018DB0BfA86aDb22d941',
                 'router': '0xED7d5F38C79115ca12fe6C0041abb22F0A06C300'},
        'ko': '0x4c191e5f7368b27Ef691f7557f60cfe0198F2075',
        'kusd': '0xd17b6d35b3159844bEe63715b7AF0517E2dfD97E',
        'usdt': '0xa71EdC38d189767582C38A3145b5873052c3e47a',
        "husd": '0x0298c2b32eaE4da002a15f36fdf7615BEa3DA047',
        'usdc': '0x9362Bbef4B8313A8Aa9f0c9808B80577Aa26B73B',
        'hbtc': '0x66a79D23E58475D2738179Ca52cd0b41d73f0BEa'
    },
    'ftm': {
        'rarity_game': '0xb3b96DF217e88Ee51513C0aBc036c3d0fC885EAA',
        'rarity_manifest': '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb',
        'bulksender': '0x4ece77753d06051e6e77bd3f021a107e88d0b636',
        'giza': '0x3389492f36642f27f7bf4a7749fb3fc2c8fbb7ee',
        'dai': '0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e',
        'spirit_swap': {
            'factory': '',
            'router': '0x16327e3fbdaca3bcf7e38f5af2599d2ddc33ae52'
        },
    }
}

STABLECOIN = {
    'heco': {'usdt': '0xa71EdC38d189767582C38A3145b5873052c3e47a',
             "husd": '0x0298c2b32eaE4da002a15f36fdf7615BEa3DA047',
             'usdc': '0x9362Bbef4B8313A8Aa9f0c9808B80577Aa26B73B'
             }
}

API_ETHERSCAN_KEY = {
}

CHAIN_API_URL = {
    "heco": "https://api.hecoinfo.com/api",
    "hecotest": "https://api-testnet.hecoinfo.com/api",
    "ftm": 'https://ftmscan.com'
}


CHAIN_PROVIDER = {
     'zksync': 'https://zksync2-mainnet.zksync.io',
    'bsc_ws': 'wss://bsc.getblock.io/mainnet/?api_key=e74d2765-ffa6-452f-a0be-aa206308ecf1',
    "heco": 'https://http-mainnet-node.huobichain.com',
    "eth":  "https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",#'http://api.zmok.io/mainnet/fkurel8hrh7yvcwz', #'https://api.mycryptoapi.com/eth',  # 'https://eth-mainnet.gateway.pokt.network/v1/5f3453978e354ab992c4da79',
    'eth_ws': 'wss://speedy-nodes-nyc.moralis.io/5b49e37f88d29b0a5e49a687/eth/mainnet/ws',
    "kovan": 'https://kovan.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161',
    "ropsten": 'https://speedy-nodes-nyc.moralis.io/5b49e37f88d29b0a5e49a687/eth/ropsten',
    "bsctest": "https://data-seed-prebsc-1-s1.binance.org:8545/",
    "bsctest_pool": ["https://data-seed-prebsc-1-s1.binance.org:8545/",
                     # "https://data-seed-prebsc-1-s1.binance.org:8545/",
                     # "https://data-seed-prebsc-1-s1.binance.org:8545/",
                     # "https://data-seed-prebsc-1-s1.binance.org:8545/",
                     # "https://data-seed-prebsc-1-s1.binance.org:8545/",
                     "https://data-seed-prebsc-1-s1.binance.org:8545/"],
    #"matic": "https://polygon-rpc.com",
    "matic": "https://polygon-pokt.nodies.app",
        "matic_pool": ['https://polygon.llamarpc.com','wss://polygon-bor-rpc.publicnode.com','https://polygon-pokt.nodies.app','https://polygon.blockpi.network/v1/rpc/public','https://api.zan.top/node/v1/polygon/mainnet/public','https://rpc-mainnet.matic.quiknode.pro','https://polygon-bor-rpc.publicnode.com','https://polygon-mainnet.rpcfast.com?api_key=xbhWBI1Wkguk8SNMu1bvvLurPGLXmgwYeC4S6g2H7WdwFigZSmPWVZRxrskEQwIf','https://polygon.meowrpc.com','https://gateway.tenderly.co/public/polygon','https://polygon.gateway.tenderly.co','https://rpc-mainnet.maticvigil.com','https://polygon.rpc.blxrbdn.com','https://polygon.drpc.org','https://rpc.ankr.com/polygon','https://polygon.api.onfinality.io/public','https://endpoints.omniatech.io/v1/matic/mainnet/public','https://polygon-mainnet.public.blastapi.io','https://1rpc.io/matic','https://polygon-rpc.com'],

    "ftm": "https://rpc.ftm.tools",
    'sol_devnet': 'https://api.devnet.solana.com',
    'sol': 'https://api.mainnet-beta.solana.com',
    'avax': 'https://api.avax.network/ext/bc/C/rpc',
    'avax_pool': ['https://speedy-nodes-nyc.moralis.io/5b49e37f88d29b0a5e49a687/avalanche/mainnet',
                  'https://api.avax.network/ext/bc/C/rpc'],
    'avaxtest': 'https://api.avax-test.network/ext/bc/C/rpc',
    'karastar': 'https://beta1-endpoint.karastar.com/',
    'kovan_pool': ['https://kovan.infura.io/v3/a5f6dcd39efe4163a16afe42b23f0b71',
                   'https://kovan.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'],
    "bsc": 'https://bsc-dataseed3.binance.org/',
    #"bsc": 'https://bsc.rpc.blxrbdn.com',
    #"bsc": 'https://bsc-dataseed.binance.org/',
    'eth_pool': ['https://1rpc.io/eth', 'https://cloudflare-eth.com',
                 'https://core.gashawk.io/rpc', 'https://endpoints.omniatech.io/v1/eth/mainnet/public',
                 'https://eth-mainnet.public.blastapi.io', 'https://eth-pokt.nodies.app', 'https://eth.drpc.org',
                 'https://eth.llamarpc.com', 'https://eth.meowrpc.com', 'https://eth.merkle.io',
                 'https://ethereum.blockpi.network/v1/rpc/public',
                 'https://ethereum.publicnode.com', 'https://rpc.ankr.com/eth', 'https://rpc.eth.gateway.fm'],
    'eth_pool': ['https://eth.llamarpc.com','https://1rpc.io/eth','https://api.securerpc.com/v1','https://api.zan.top/node/v1/eth/mainnet/public','https://api.zmok.io/mainnet/oaen6dy8ff6hju9k','https://cloudflare-eth.com','https://core.gashawk.io/rpc','https://endpoints.omniatech.io/v1/eth/mainnet/public','https://eth-mainnet.nodereal.io/v1/1659dfb40aa24bbb8153a677b98064d7','https://eth-mainnet.rpcfast.com?api_key=xbhWBI1Wkguk8SNMu1bvvLurPGLXmgwYeC4S6g2H7WdwFigZSmPWVZRxrskEQwIf','https://eth-pokt.nodies.app','https://eth.drpc.org','https://eth.meowrpc.com','https://eth.merkle.io','https://eth.nodeconnect.org','https://eth.rpc.blxrbdn.com','https://ethereum.blockpi.network/v1/rpc/public','https://ethereum.publicnode.com','https://gateway.tenderly.co/public/mainnet','https://go.getblock.io/d7dab8149ec04390aaa923ff2768f914','https://mainnet.gateway.tenderly.co','https://rpc.ankr.com/eth','https://rpc.builder0x69.io','https://rpc.eth.gateway.fm','https://rpc.flashbots.net','https://rpc.flashbots.net/fast','https://rpc.lokibuilder.xyz/wallet','https://rpc.mevblocker.io','https://rpc.mevblocker.io/fast','https://rpc.mevblocker.io/fullprivacy','https://rpc.mevblocker.io/noreverts','https://rpc.notadegen.com/eth','https://rpc.payload.de'],
    'bsc_pool': [ 'https://bsc-mainnet.nodereal.io/v1/64a9df0874fb4a93b9d0a3849de012d3',
                 'https://bsc.blockpi.network/v1/rpc/public', 'https://bscrpc.com', 'https://bsc-pokt.nodies.app',
                 'https://binance.nodereal.io', 'https://bsc-dataseed4.bnbchain.org',
                 'https://bsc-dataseed.bnbchain.org', 'https://bsc.drpc.org', 'https://bsc.publicnode.com',
                 'https://bsc-mainnet.public.blastapi.io', 'https://bsc-dataseed3.ninicoin.io',
                 'https://bsc-dataseed2.bnbchain.org', 'https://bsc-dataseed1.defibit.io',
                 'https://bsc-dataseed2.ninicoin.io', 'https://bsc-dataseed4.ninicoin.io',
                 'https://bsc-dataseed1.bnbchain.org', 'https://bsc-dataseed1.ninicoin.io',
                 'https://bsc-dataseed2.defibit.io', 'https://bsc-dataseed3.defibit.io',
                 'https://bsc-dataseed4.defibit.io', 'https://bsc-dataseed3.bnbchain.org',
                 'https://koge-rpc-bsc.48.club', 'https://rpc-bsc.48.club'],

    # 'bsc_pool': ['https://bsc-dataseed.binance.org/',
    #               'https://bsc-dataseed4.defibit.io/', ],
    'rinkeby': 'https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161',
    'gate': 'https://evm.gatenode.cc',
    'gate_test': 'https://meteora-evm.gatenode.cc',
    'arbitrum_goerli': 'https://goerli-rollup.arbitrum.io/rpc',
    "arbitrum": 'https://arb1.arbitrum.io/rpc',
    'goerli': 'https://rpc.ankr.com/eth_goerli'


}

""" 
"""
BlockNativeKey = [
]

TenderlyKey = [' ']

SNIPER = {
    'bsc': ' '
}

#   mykey
OpenseaKey = [' ']
MoralisKey = [' ']

MYSQL_CONF = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Gatesec@2023',
    'db': 'risk_control'
}

MYSQL_CONFx = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'swapbot'
}

EOA = [
    {'address': '0x89E86Fab421DAf84934D0F1Ce2A7628f26A036c4', 'privatekey': '1953b9ffc5ace1ecb6d3e3995da64bfbab4cdd8e644e39a9a18ac3c07faec302'}
]

main_coin_lst = ['bsc_WBNB', 'bsc_USDT', 'bsc_BUSD',
                     'eth_USDT', 'eth_WETH', 'eth_WBTC']
THREADCOUNT = 30
