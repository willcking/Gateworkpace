
from decimal import Decimal
import threading
import multiprocessing

from dbutils.pooled_db import PooledDB
import MySQLdb

from common import orm
from core.libs import get_logger
from wconfig import CONTRACT_ADDRESS, main_coin_lst

logger = get_logger('retrive_pairinfo.log')


db_lock = threading.Lock()

db_pool = PooledDB(
    creator=MySQLdb,  # 假设你使用的是MySQL数据库
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='swapbot',
    maxconnections=10,  # 设置最大连接数
    blocking=True  # 设置为阻塞模式，避免数据库连接死锁
)



def update_token_db_price(network, address, price):
    logger.info(f'writting db token price {address} : {price}')
    if network == 'bsc':
        network = 'BSC'
    if network == 'eth':
        network = 'ETH'


    with db_pool.connection() as conn:
        cursor = conn.cursor()
        with db_lock:  # use the 'with' statement to acquire and release the lock
            # 执行数据库更新操作
            q = """
            UPDATE coin_lists SET dex_price = %s where network = %s and token_address = %s
            """
            cursor.execute(q, (Decimal(price), network, address))
            conn.commit()
        cursor.close()


def calc_token_db_price(pair_obj):

    main_token_lst = []
    for i in main_coin_lst:
        main_token_lst.append(i.split('_')[1].lower())
    # 查询Token表中的所有记录
    query = orm.Token.select().where(orm.Token.maincoin== 1)
    quote_list = []
    # 遍历查询结果
    for token in query:
        # 打印出每个记录的symbol字段和price字段
        logger.info(f"quotetoken: {token.symbol}, {token.price}, {token.address}")
        quote_list.append(token.address)

    #for pair_obj in orm.Pair().select():
    if pair_obj.reserve0 > 0 and pair_obj.reserve1>0:
        logger.info(f'updating   {pair_obj.network}  app:  {pair_obj.app}  addr: {pair_obj.pair}')
        quote_token = pair_obj.token0 if pair_obj.token0  in quote_list else pair_obj.token1
        quote_token_reserve = pair_obj.reserve0 if pair_obj.token0  in quote_list else pair_obj.reserve1

        base_token = pair_obj.token0 if pair_obj.token1 == quote_token else pair_obj.token1
        base_token_reserve = pair_obj.reserve0 if pair_obj.token1 == quote_token else pair_obj.reserve1

        quote_token_obj = orm.Token.get(orm.Token.address == quote_token, orm.Token.network ==pair_obj.network )
        base_token_obj = orm.Token.get(orm.Token.address == base_token)

        logger.info(f'base token {base_token_obj.symbol}  quote token {quote_token_obj.symbol} {quote_token_obj.price}')
        base_price = quote_token_obj.price * Decimal(quote_token_reserve) / 10** int(quote_token_obj.decimal) * 10** int(base_token_obj.decimal)/ base_token_reserve
        logger.info(f"{base_token_obj.symbol},  {base_price}, {base_token_obj.address}")
        return pair_obj.network, base_token_obj.address, base_price
        # if base_token_obj.symbol.lower() in main_token_lst:
        #     logger.info(f"ignore main token {quote_token_obj.symbol}")
        #
        # else:
            #update_token_db_price(pair_obj.network , base_token_obj.address, base_price)
    #return pair_obj.network, base_token_obj.address, base_price
    return 1


def calc_price():
    main_token_lst = [i.split('_')[1].lower() for i in main_coin_lst]
    quote_list = [token.address for token in orm.Token.select().where(orm.Token.maincoin == 1)]

    pair_objs = [pair_obj for pair_obj in orm.Pair().select() if pair_obj.reserve0 > 0 and pair_obj.reserve1 > 0]

    # Set up the multiprocessing pool
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    #pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    # Use pool.map to apply the function to the list of pair_objs
    pool.map(calc_token_db_price, pair_objs)

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

if __name__ == '__main__':
    calc_price()