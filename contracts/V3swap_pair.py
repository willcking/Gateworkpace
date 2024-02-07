
from core.contract import Contract
from core.libs import AddressType
from core.libs import load_abi

from common import orm
class V3SwapPairContract(Contract):
    def __init__(self,
                 app_name: str,
                 chain,
                 pair_address: AddressType
                 ) -> None:
        self.app_name = app_name
        self.address = chain.w3.to_checksum_address(pair_address)
        self.chain = chain
        self.abi = load_abi('uniV3/pair.json')
        self.contract = chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def get_tokens_from_pair(self, ):
        token0 = self.contract.functions.token0().call()
        token1 = self.contract.functions.token1().call()
        return (token0, token1)

    def get_fee(self):
        fee = self.contract.functions.fee().call()
        return  fee

    def get_reserve_from_pair(self, ):
        self.logger.debug(f'updating reserve : {self.address}')

        (amount0, amount1, x) = self.contract.functions.getReserves().call()
        return (amount0, amount1)


    def get_tokens_from_db(self):
        p = orm.Pair().get_or_none(orm.Pair.network == self.chain.chain_name, orm.Pair.pair == self.address)
        return (p.token0, p.token1)

    def get_reserves_from_db(self):
        p = orm.Pair().get_or_none(orm.Pair.network == self.chain.chain_name, orm.Pair.pair == self.address)
        return (p.reserve0, p.reserve1)


    def get_tick(self, ):
        sqrtPriceX96, tick,b,c,d,e,f = self.contract.functions.slot0().call()
        return tick

    def get_P(self, ):
        (sqrtPriceX96, tick, observationIndex, observationCardinality, feeProtocol,
         unlocked,f) = self.contract.functions.slot0().call()
        #price = int(sqrtPriceX96) ** 2 * 10 ** 18 // (2 ** 192)
        price = (sqrtPriceX96 * sqrtPriceX96) * 10**18 >> (96 * 2)
        return price
