# 只寻找主流币之间的差价

from common.chainutils import update_maincoin_price,store_pair_from_chain
from common.update_chainlist import update_chains
def run(status):
    if status == 0:
        try:
            update_chains(1)
        except Exception as e:
            print(e)
        update_maincoin_price()
        store_pair_from_chain()

if __name__ == '__main__':
    run(0)
