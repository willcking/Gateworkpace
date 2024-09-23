from decimal import Decimal
from peewee import DoesNotExist
from contracts.erc20 import ERC20Contract
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from common import orm
from contracts.swap_pair import SwapPairContract
from core.chain_network import ChainNetworkNew
from core.libs import get_logger
from wconfig import  THREADCOUNT,CHAIN_PROVIDER
from datetime import datetime
from contracts.V3swap_quoter import V3SwapQuote
from web3.exceptions import ContractLogicError
from common.update_chainlist import read_nodes_from_config
import random
import requests

logger = get_logger('retrive_pairinfo.log')
main_coin_lst = ['bsc_WBNB', 'bsc_USDT', 'bsc_BUSD',
                     'eth_USDT', 'eth_WETH', 'eth_WBTC']
error_update_list = []

orm.database.connect()
main_token_contract_list = {token.address for token in orm.Token.select(orm.Token.address).where(orm.Token.maincoin == 1)}
main_token_lst = [i.split('_')[1].lower() for i in main_coin_lst]

main_token_prices = {'busd': 1,
                     'usdt': 1,
                     'usdc': 1}

eth_providerlist = read_nodes_from_config()
bsc_providerlist = CHAIN_PROVIDER['bsc_pool']

for symbol in ['wbnb', 'weth', 'wbtc']:
    coinlist_obj = orm.CoinLists.get_or_none(orm.CoinLists.symbol == symbol.upper()[1:])
    if coinlist_obj is not None:
        main_token_prices[symbol] = coinlist_obj.gate_price or 0

orm.database.close()


def upsert_pair_info(network, pair_address, liquidity, symbol, token_address):
    # 查询是否存在具有相同network和pair_address的记录
    query = orm.PairInfo.select().where(orm.PairInfo.network == network, orm.PairInfo.pair_address == pair_address)
    if query.exists():
        # 存在相同的记录，进行更新
        pair_info = query.get()
        pair_info.last_update_at = pair_info.update_at
        pair_info.last_liquidity = pair_info.liquidity
        pair_info.liquidity = liquidity
        pair_info.update_at = datetime.now()
        pair_info.save()
    else:
        # 不存在相同的记录，创建新的记录
        orm.PairInfo.create(
            network=network,
            symbol =symbol,
            token_address = token_address,
            pair_address=pair_address,
            liquidity=liquidity,
            update_at=datetime.now(),
            last_update_at=None,  # 或者可以设置为当前时间，根据实际需求而定
            last_liquidity=None  # 同上
        )

    # data = {
    #     'network': network,  # 示例值，实际应用中请替换为具体值
    #     'pair_address': pair_address,  # 示例值，实际应用中请替换为具体值
    #     'liquidity': float(liquidity),  # 示例值，实际应用中请替换为具体值
    #     'symbol': symbol,  # 示例值，实际应用中请替换为具体值
    #     'token_address': token_address  # 示例值，实际应用中请替换为具体值
    # }




def get_main_token_price(quote_token_symbol):
    try:
        if quote_token_symbol.lower() in main_token_lst:
            return main_token_prices[quote_token_symbol.lower()]
        elif quote_token_symbol.upper() in ('USDT', 'BUSD'):
            return 1
        else:
            quote_token_obj = orm.Token.get_or_none(
                orm.Token.symbol == quote_token_symbol.upper(),
                orm.Token.network == 'BSC',
            )
            if quote_token_obj is not None:
                return quote_token_obj.price or 0
            else:
                return 0
    except Exception as e:
        logger.error(f'error get maintoken price {e}')
        return 0

def update_pair_reserve(pair_obj, network):
    if pair_obj.pair != '0x12CC685eEb95D3fCDfAe0a996e214e51FA6f7548':
       return
    quote_token = pair_obj.token0 if pair_obj.token0 in main_token_contract_list else pair_obj.token1
    base_token = pair_obj.token0 if pair_obj.token1 == quote_token else pair_obj.token1
    logger.info(f"{pair_obj.app} {base_token} / {quote_token}")
    liqU = 0
    token0_balance = 0
    token1_balance = 0
    if quote_token in main_token_contract_list and base_token in main_token_contract_list:
        logger.error('both main token')
        return

    if quote_token not in main_token_contract_list and base_token not in main_token_contract_list:
        logger.error('both not main token')
        return

    if network  == 'eth':
        provider = random.choice(eth_providerlist)
    if network == 'bsc':
        provider = random.choice(bsc_providerlist)

    logger.info(provider)
    chain = ChainNetworkNew(chain_name=network, provider=provider)

    quote_token_obj = orm.Token.get_or_none(
        orm.Token.address == quote_token,
        orm.Token.network == pair_obj.network
    )

    base_token_obj = orm.Token.get_or_none(
        orm.Token.address == base_token,
        orm.Token.network == pair_obj.network
    )

    if (quote_token_obj is None) or (base_token_obj is None):
        return

    main_coin_price = get_main_token_price(quote_token_obj.symbol)

    if main_coin_price == 0:
        logger.error('get main coin price =0')
        return

    if pair_obj.app in ('uni_swap', 'pancake_swap','sushiswap', 'uniswapv3'):
        try:
            quote_contract = ERC20Contract(chain=chain, token_addr=quote_token_obj.address)
            quote_balance = quote_contract.balance(pair_obj.pair)
            quote_balance = quote_balance / 10**int(quote_token_obj.decimal)
            liqU = quote_balance * float(main_coin_price)
            logger.info(liqU)

            logger.info(f"{pair_obj.app } liq: {liqU} quote:{quote_token_obj.symbol}   base:{base_token_obj.symbol}, basetoken:{base_token_obj.address}")

        except Exception as e:
            logger.error(f"Error updating liq : {e}")
            if pair_obj.id not in error_update_list:
                error_update_list.append(pair_obj.id)
    else:
        return

    if liqU > 0:
        try:
            # # 使用ORM更新数据库
            # pair = orm.PairInfo.get(
            #     orm.PairInfo.network == network,
            #     orm.PairInfo.pair_address == pair_obj.pair
            # )

            upsert_pair_info(
                network=pair_obj.network.upper(),
                pair_address=pair_obj.pair,
                symbol=base_token_obj.symbol,
                token_address=base_token_obj.address,
                liquidity=Decimal(liqU),
                #volume_24h=Decimal('5000.00'),
                #last_update_at=date.today(),
                # last_liquidity=Decimal('9500.00')
            )
        except DoesNotExist:
            logger.error(f"Pair not found in the database: {network} {pair_obj.app} {pair_obj.pair}")
        except Exception as e:
            logger.error(f"Error updating pair reserve: {e}")

def update_all_token_reserve(network):
    logger.debug('updating reserve...')
    pair_objs = orm.Pair.select().where(
        ((orm.Pair.app == 'uni_swap') & (orm.Pair.network == network)) |
        ((orm.Pair.app == 'uniswapv3') & (orm.Pair.network == network)) |
        ((orm.Pair.app == 'pancake_swap') & (orm.Pair.network == network))|
        ((orm.Pair.app == 'sushiswap') & (orm.Pair.network == network))
    )

    logger.debug(f'total {len(pair_objs)}')
    THREADCOUNT = 1
    with ThreadPoolExecutor(max_workers=THREADCOUNT) as executor:
        for pair_obj in pair_objs:
            executor.submit(update_pair_reserve, pair_obj, network)


def signal_done():
    # 目标URL
    url = 'http://127.0.0.1:45612/comparison?status=success'

    # 发送POST请求
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        logger.info('http req faild')
    else:
        logger.error('http req faild')

if __name__ == '__main__':
    for net in ['bsc', 'eth']:
        orm.database.connect()  # 连接数据库
        update_all_token_reserve(net)
        orm.database.close()  # 关闭数据库连接

    signal_done()

