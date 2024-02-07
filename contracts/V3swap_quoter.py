
from core.contract import Contract
from core.libs import AddressType
from core.libs import load_abi

from common import orm
from wconfig import CONTRACT_ADDRESS

class V3SwapQuote(Contract):
    def __init__(self,
                 app_name: str,
                 chain,
                 #pair_address: AddressType
                 ) -> None:
        self.app_name = app_name
        self.address = chain.w3.to_checksum_address(CONTRACT_ADDRESS[chain.chain_name]['uniswapv3']['quoter'])
        self.chain = chain
        self.abi = load_abi('uniV3/quoter.json')
        self.contract = chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def get_tokens_from_pair(self, ):
        token0 = self.contract.functions.token0().call()
        token1 = self.contract.functions.token1().call()
        return (token0, token1)


    def get_reserve_from_pair(self, ):
        self.logger.debug(f'updating reserve : {self.address}')

        (amount0, amount1, x) = self.contract.functions.getReserves().call()
        return (amount0, amount1)


    def get_tokens_from_db(self):
        p = orm.Pair().get_or_none(orm.Pair.network == self.chain.chain_name, orm.Pair.pair == self.address)
        return (p.token0, p.token1)



    def get_tick(self, ):
        sqrtPriceX96, tick,b,c,d,e,f = self.contract.functions.slot0().call()
        return tick

    def quoteExactInputSingle(self, tokenIn, tokenOut, amount_in, fee):
        FEE = int(fee)
        SQRT_PRICE_LIMIT = 0
        amount_out = self.contract.functions.quoteExactInputSingle(tokenIn, tokenOut, FEE, amount_in, SQRT_PRICE_LIMIT).call()
        return amount_out