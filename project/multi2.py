from decimal import Decimal
from peewee import DoesNotExist
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

logger = get_logger('retrive_pairinfo.log')
main_coin_lst = ['bsc_WBNB', 'bsc_USDT', 'bsc_BUSD',
                 'eth_USDT', 'eth_WETH', 'eth_WBTC', 'matic_WMATIC', 'matic_WETH']

error_update_list = []

orm.database.connect()
main_token_contract_list = {token.address for token in orm.Token.select(orm.Token.address).where(orm.Token.maincoin == 1)}
main_token_lst = [i.split('_')[1].lower() for i in main_coin_lst]

main_token_prices = {'busd': 1,
                     'usdt': 1,
                     'usdc': 1}

eth_providerlist = read_nodes_from_config()
bsc_providerlist = CHAIN_PROVIDER['bsc_pool']
matic_providerlist = CHAIN_PROVIDER['matic_pool']

for symbol in ['wbnb', 'weth', 'wbtc', 'wmatic']:
    coinlist_obj = orm.CoinLists.get_or_none(orm.CoinLists.symbol == symbol.upper()[1:])
    if coinlist_obj is not None:
        main_token_prices[symbol] = coinlist_obj.gate_price or 0

orm.database.close()
def get_main_token_price(quote_token_symbol):
    try:
        if quote_token_symbol.lower() in main_token_lst:
            return main_token_prices[quote_token_symbol.lower()]
        elif quote_token_symbol.upper() in ('USDT', 'BUSD', 'USDC'):
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
    quote_token = pair_obj.token0 if pair_obj.token0 in main_token_contract_list else pair_obj.token1
    base_token = pair_obj.token0 if pair_obj.token1 == quote_token else pair_obj.token1
    logger.info(f"{pair_obj.app} {base_token} / {quote_token}")
    base_coin_price = 0
    token0_balance = 0
    token1_balance = 0
    if quote_token in main_token_contract_list and base_token in main_token_contract_list:
        logger.error('both main token')
        return

    if quote_token not in main_token_contract_list and base_token not in main_token_contract_list:
        logger.error('both not main token')
        return

    provider = random.choice(eval(network+'_providerlist'))


    logger.info(provider)
    chain = ChainNetworkNew(chain_name=network, provider=provider)

    quote_token_obj = orm.Token.get_or_none(
        orm.Token.address == quote_token,
        #orm.Token.network == pair_obj.network
    )

    base_token_obj = orm.Token.get_or_none(
        orm.Token.address == base_token,
    #   orm.Token.network == pair_obj.network
    )

    if (quote_token_obj is None) or (base_token_obj is None):
        return

    if pair_obj.app == 'uniswapv3' and pair_obj.network != 'matic':
        try:
            quote_contract = V3SwapQuote(app_name=pair_obj.app, chain=chain)

            coinlist_obj = orm.CoinLists.get_or_none(
                orm.CoinLists.token_address == base_token,
                orm.CoinLists.network == network.upper()
            )

            if coinlist_obj is None:
                logger.error('error CoinLists record none')
                return
            if coinlist_obj.gate_price is None:
                logger.error('error CoinLists gate price is  none')
                return

            amount_in = int(100 / coinlist_obj.gate_price * 10 ** int(base_token_obj.decimal))
            amount_out = quote_contract.quoteExactInputSingle(base_token, quote_token, amount_in, pair_obj.fee)

            main_coin_price = get_main_token_price(quote_token_obj.symbol)
            logger.info(f'main coin price {main_coin_price}')

            if main_coin_price == 0:
                return

            base_coin_price = Decimal(main_coin_price) *  Decimal(amount_out) /  10 ** int(quote_token_obj.decimal) /  (Decimal(amount_in) / 10 ** int(base_token_obj.decimal) )

            # base_coin_price = Decimal(amount_out) * 10 ** int(quote_token_obj.decimal) / amount_in / 10 ** int(base_token_obj.decimal) \
            #         * Decimal(main_coin_price)

            logger.info(
                f"{pair_obj.app} {base_token_obj.symbol}/{quote_token_obj.symbol} {base_coin_price} basetoken:{base_token_obj.address}"
            )

            if pair_obj.id in error_update_list:
                error_update_list.remove(pair_obj.id)
        except ValueError as e:
            # 处理 ValueError 异常
            base_coin_price = 0
            logger.error(f"Error updating v3 price: {e}")
            if pair_obj.id in error_update_list:
                error_update_list.remove(pair_obj.id)

        except ZeroDivisionError as e:
            # 处理除零异常
            base_coin_price = 0
            logger.error(f"Error updating v3 price: {e}")
            if pair_obj.id in error_update_list:
                error_update_list.remove(pair_obj.id)
        except ContractLogicError as e:
            # 处理除零异常
            base_coin_price = 0
            logger.error(f"Error updating v3 price: {e}")
            if pair_obj.id in error_update_list:
                error_update_list.remove(pair_obj.id)
        except Exception as e:
            logger.error(f"Error updating v3 price: {e}")

            if pair_obj.id not in error_update_list:
                error_update_list.append(pair_obj.id)

    elif pair_obj.app in ('uni_swap', 'pancake_swap','sushiswap', 'quickswapv2'):
        try:
            pair_contract = SwapPairContract(app_name=pair_obj.app, chain=chain, pair_address=pair_obj.pair)
            (token0_balance, token1_balance) = pair_contract.get_reserve_from_pair()

            quote_token_reserve = token0_balance if pair_obj.token0 in main_token_contract_list else token1_balance
            base_token_reserve = token0_balance if pair_obj.token1 == quote_token else token1_balance

            if token0_balance <= 0 or token1_balance <= 0:
                return

            main_coin_price = get_main_token_price(quote_token_obj.symbol)

            if main_coin_price == 0:
                logger.error('get main coin price =0')
                return

            base_coin_price = main_coin_price * Decimal(quote_token_reserve) / 10 ** int(
                quote_token_obj.decimal) * 10 ** int(base_token_obj.decimal) / base_token_reserve

            logger.info(f"v2 {chain.chain_name} {pair_obj.app} {base_token_obj.symbol},quotereserve {quote_token_reserve} basereserve {base_token_reserve},  {base_coin_price} basetoken:{base_token_obj.address}")

            if pair_obj.id in error_update_list:
                error_update_list.remove(pair_obj.id)
        except ValueError as e:
            # 处理 ValueError 异常
            base_coin_price = 0
            logger.error(f"Error updating v3 price: {e}")
            if pair_obj.id in error_update_list:
                error_update_list.remove(pair_obj.id)

        except ZeroDivisionError as e:
            # 处理除零异常
            base_coin_price = 0
            logger.error(f"Error updating v3 price: {e}")
            if pair_obj.id in error_update_list:
                error_update_list.remove(pair_obj.id)

        except ContractLogicError as e:
            # 处理除零异常
            base_coin_price = 0
            logger.error(f"Error updating v3 price: {e}")
            if pair_obj.id in error_update_list:
                error_update_list.remove(pair_obj.id)

        except Exception as e:
            logger.error(f"Error updating v2 price: {e}")
            if pair_obj.id not in error_update_list:
                error_update_list.append(pair_obj.id)
    else:
        return

    if base_coin_price > 0:
        try:
            # 使用ORM更新数据库
            pair = orm.Pair.get(
                orm.Pair.network == network,
                orm.Pair.app == pair_obj.app,
                orm.Pair.pair == pair_obj.pair
            )
            pair.reserve0 = Decimal(token0_balance)
            pair.reserve1 = Decimal(token1_balance)
            pair.rate = Decimal(base_coin_price)
            pair.updatetime = datetime.now()
            pair.save()
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
        ((orm.Pair.app == 'sushiswap') & (orm.Pair.network == network))|
        ((orm.Pair.app == 'quickswapv2') & (orm.Pair.network == network))
    )

    logger.debug(f'total {len(pair_objs)}')

    with ThreadPoolExecutor(max_workers=THREADCOUNT) as executor:
        for pair_obj in pair_objs:
            executor.submit(update_pair_reserve, pair_obj, network)


def check_error_pair():
    orm.database.connect()
    logger.debug('updating error reserve...')
    while len(error_update_list) > 0:
        logger.debug(f'total error {len(error_update_list)}')
        for i in error_update_list:
            pair_obj = orm.Pair.get_by_id(i)

            update_pair_reserve(pair_obj=pair_obj, network=pair_obj.network)

    orm.database.close()

if __name__ == '__main__':
    for net in ['matic', 'eth', 'bsc']:
        orm.database.connect()  # 连接数据库
        update_all_token_reserve(net)
        orm.database.close()  # 关闭数据库连接



    check_error_pair()
