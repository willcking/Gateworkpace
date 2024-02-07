 
import json
from common.exchangelib import get_gate_price
from web3 import Web3
from decimal import Decimal


from common import orm
from contracts.erc20 import ERC20Contract
from contracts.swap_factory import SwapFactoryContract
from contracts.swap_pair import SwapPairContract
from core.chain_network import ChainNetwork
from core.libs import get_logger
from wconfig import CONTRACT_ADDRESS
from wconfig import EOA

logger = get_logger('retrive_pairinfo.log')


def update_maincoin_price():

    p = 0
    main_coin_lst = []

    for i in main_coin_lst:
        token = i.split('_')[1]
        chain = i.split('_')[0]
        if token == 'WBNB':
            p = get_gate_price('BNB_USDT')
        if token == 'WBTC':
            p = get_gate_price('BTC_USDT')
        if token == 'USDT':
            p = 1
        if token == 'BUSD':
            p = 1
        if token == 'WETH':
            p = get_gate_price('ETH_USDT')
        if token == 'WBTC':
            p = get_gate_price('BTC_USDT')

        if p !=  0:
            logger.info(f" update price {i} {p}")
            q = orm.Token.update({
                'price': p,
                'maincoin': 1
            }).where(orm.Token.network == chain, orm.Token.symbol == token)
            q.execute()

def format_input(app, chain):
    app1 = app
    chain1 = chain

    if app == 'uniswapv2':
        app1 = 'uni_swap'
    if app == 'pancakeswapv2':
        app1 = 'pancake_swap'
    if app == 'sushiswap':
        app1 = 'sushi_swap'

    if chain == 'ETH':
        chain1 = 'eth'
    if chain == 'BSC':
        chain1 = 'bsc'
    return app1, chain1

def store_pair_from_chain():
    #chain_ = ChainNetwork('eth')
    # 获取所有的coin_lists行
    coin_lists_rows = orm.CoinLists.select().where((orm.CoinLists.dex.is_null(False)) & (orm.CoinLists.pair_address.is_null(False))
)
    coin_lists_rows = orm.CoinLists.select().where( orm.CoinLists.id ==3
        )

    # 遍历coin_lists行
    for row in coin_lists_rows:
        l = [row.token_address, row.symbol, row.network, row.dex, row.pair_address, row.gate_price, row.dex_price]
        logger.info(str(l))
        if row.network + '_' + row.dex  in [
            'ETH_uniswapv2',
            'ETH_uniswapv3',
            'BSC_pancakeswapv2',
            'ETH_sushiswap',
        ]:
            logger.info([row.token_address, row.symbol, row.network, row.dex, row.pair_address, row.gate_price, row.dex_price])

            app, chain = format_input(row.dex, row.network)
            try:
                #address = chain_.w3.to_checksum_address(row.pair_address)
                if not orm.Pair().get_or_none(orm.Pair.network == chain, orm.Pair.app == app,
                                       orm.Pair.pair == row.pair_address):
                    chain = ChainNetwork(chain)
                    pair_contract = SwapPairContract(app_name=app, chain=chain, pair_address=row.pair_address)
                    store_pair_info(pair_contract, uid=0)

            except Exception as e:
                print(e)



# 根据token1 token0 获取pair 地址 并存储
def print_pair(network, newapp, oldapp):
    BaseTokens = ['WBNB', 'USDC', 'USDT', 'BUSD']

    pairs_list = []
    for pair_obj1 in orm.Pair().select().where(orm.Pair.network == network, orm.Pair.app == oldapp).iterator():
        pair_obj2 = orm.Pair().get_or_none(orm.Pair.network == network, orm.Pair.app == newapp,
                                           orm.Pair.token0 == pair_obj1.token0, orm.Pair.token1 == pair_obj1.token1)
        if pair_obj2:
            if (pair_obj1.token0symbol in BaseTokens) or (pair_obj1.token1symbol in BaseTokens):
                D = {'symbols': '', "pairs": []}
                pair_symbol = f'{pair_obj1.token0symbol}-{pair_obj1.token1symbol}'
                D['symbols'] = pair_symbol
                pairs = [pair_obj1.pair, pair_obj2.pair]
                D['pairs'] = pairs
                pairs_list.append(D)

    print(json.dumps(pairs_list))
    print(pairs_list)


def store_pair_info(pair_contract: SwapPairContract, uid):
    (token0, token1) = pair_contract.get_tokens_from_pair()
    logger.info([pair_contract.address, token0, token1])
    try:
        token0_contract = ERC20Contract(chain=pair_contract.chain, token_addr=token0)
        store_token_detail(address=token0_contract.address, network=pair_contract.chain.chain_name, symbol=token0_contract.token_symbol,
                           decimal=token0_contract.token_decimals)
        token1_contract = ERC20Contract(chain=pair_contract.chain, token_addr=token1)
        store_token_detail(address=token1_contract.address, network=pair_contract.chain.chain_name, symbol=token1_contract.token_symbol,
                           decimal=token1_contract.token_decimals)
    except Exception as e:
        logger.error(e)

    if orm.Pair.get_or_none(pair=pair_contract.address, app=pair_contract.app_name):
        logger.info('pair exsit')
        return
    else:
        if pair_contract.app_name == 'uniswapv3':

            logger.info('save v3')
            fee = pair_contract.get_fee()
            note1 = orm.Pair.create(uid=uid, network=pair_contract.chain.chain_name, app=pair_contract.app_name,
                                    pair=pair_contract.address, token0=token0, token1=token1,
                                    token0symbol=token0_contract.token_symbol, token1symbol=token1_contract.token_symbol, fee=fee)
            note1.save()
        else:
            logger.info('save v2')
            note1 = orm.Pair.create(uid=uid, network=pair_contract.chain.chain_name, app=pair_contract.app_name,
                                    pair=pair_contract.address, token0=token0, token1=token1,
                                    token0symbol=token0_contract.token_symbol, token1symbol=token1_contract.token_symbol)
            note1.save()


def store_token_detail(address: str, network: str, symbol: str, decimal: str):
    if orm.Token.get_or_none(address=address, network=network):
        pass
    else:
        logger.info(f'new token {address} on {network}')
        note1 = orm.Token.create(network=network, address=address, symbol=symbol, decimal=decimal)
        note1.save()



def update_all_token_reserve(network):
    logger.info('updating reserve...')
    chain = ChainNetwork(network)
    #if fast == 1:
    for pair_obj in orm.Pair().select().where(orm.Pair.network == network).iterator():
            logger.info(f'updating reserve : {network}  app:  {pair_obj.app}  index: {pair_obj.uid}')
            pair_contract = SwapPairContract(app_name=pair_obj.app, chain=chain, pair_address=pair_obj.pair)
            (token0_balance, token1_balance) = pair_contract.get_reserve_from_pair()
            q = orm.Pair.update({
                'reserve0': Decimal(token0_balance),
                'reserve1': Decimal(token1_balance)
            }).where(orm.Pair.network == network, orm.Pair.app == pair_obj.app, orm.Pair.pair == pair_obj.pair)
            q.execute()





if __name__ == '__main__':
    network = 'heco'
    app1 = 'bxh'
    app2 = 'mdex'


