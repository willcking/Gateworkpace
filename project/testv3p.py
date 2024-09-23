import threading

from decimal import Decimal
from dbutils.pooled_db import PooledDB
import MySQLdb
from concurrent.futures import ThreadPoolExecutor
from common.calc_db_price import calc_token_db_price
from common import orm
from contracts.V3swap_pair import V3SwapPairContract
from contracts.V3swap_quoter import V3SwapQuote
from core.chain_network import  ChainNetworkNew
from core.libs import get_logger
from common.erc20 import ERC20Contract

from wconfig import main_coin_lst, MYSQL_CONF
import  time


logger = get_logger('retrive_pairinfo.log')
db_lock = threading.Lock()


db_pool = PooledDB(
    creator=MySQLdb,  # 假设你使用的是MySQL数据库
    host=MYSQL_CONF['host'],
    port=3306,
    user=MYSQL_CONF['user'],
    password='',
    database=MYSQL_CONF['db'],
    maxconnections=10,  # 设置最大连接数
    blocking=True  # 设置为阻塞模式，避免数据库连接死锁
)


def update_pair_price(pair_obj, network):
    #network = 'eth'
    chain = ChainNetworkNew(network)
    main_coin_list = [token.address for token in orm.Token.select().where(orm.Token.maincoin == 1)]
    # 0x111111111117dc0aa78b770fa6a738034120c302 1INCH ETH uniswapv3 0xE931b03260B2854e77e8dA8378A1BC017b13cb97 None None
    app = 'uniswapv3'
    pair_contract = V3SwapPairContract(app_name=app, chain=chain, pair_address=pair_obj.pair)
    token0_addr, token1_addr = pair_contract.get_tokens_from_db()

    base_token = token0_addr if token1_addr in main_coin_list else token1_addr
    quote_token = token1_addr if base_token == token0_addr else token0_addr

    base_token_obj = ERC20Contract(chain=network, contract_addr=base_token)
    quote_token_obj = ERC20Contract(chain=network, contract_addr=quote_token)

    quote_contract = V3SwapQuote(app_name=app, chain=chain)

    fee = pair_contract.get_fee()
    #算100u的
    gate_price = orm.CoinLists.get(orm.CoinLists.token_address == base_token, orm.CoinLists.network ==  network.upper()).gate_price
    if gate_price is None:
        print('error gate price none')
    amount_in =  int(100/ gate_price *  10**base_token_obj.token_decimals)
    amount_out = quote_contract.quoteExactInputSingle(base_token, quote_token, amount_in, fee)

    #logger.info(amount_in, amount_out)

    with db_pool.connection() as conn:
        cursor = conn.cursor()
        with db_lock:
            quote_token_obj_db = orm.Token.get(orm.Token.address == quote_token, orm.Token.network == network)

            price =  Decimal(amount_out) *  10** quote_token_obj.token_decimals  / amount_in / 10** base_token_obj.token_decimals *  Decimal(quote_token_obj_db.price)
            logger.info(f"{base_token_obj.token_symbol}/{quote_token_obj.token_symbol} {price} basetoken:{base_token_obj.contract_addr} ")

            q = """
            UPDATE Pair SET  rate = %s WHERE network = %s AND app = %s AND pair = %s
            """
            cursor.execute(q,  (price, network, pair_obj.app, pair_obj.pair))
            conn.commit()
        cursor.close()

def update_all_token_price(network):
    logger.info('updating v3 price...')
    pair_objs = orm.Pair().select().where(orm.Pair.network == network, orm.Pair.app=='uniswapv3')

    # Define the number of worker threads
    num_worker_threads = 1

    # Create a ThreadPoolExe1utor
    with ThreadPoolExecutor(max_workers=num_worker_threads) as executor:
        # Submit tasks to the executor
        for pair_obj in pair_objs:
            #logger.info(f"app: {pair_obj.app} addr: {pair_obj.pair}  ")
            executor.submit(update_pair_price, pair_obj, network)


if __name__ == '__main__':
    network = 'eth'
    update_all_token_price(network)