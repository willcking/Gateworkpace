
from core.contract import Contract
from core.libs import AddressType
from core.libs import load_abi

class SwapPairContract(Contract):
    def __init__(self,
                 app_name: str,
                 chain,
                 pair_address: AddressType
                 ) -> None:
        self.app_name = app_name
        self.address = chain.w3.to_checksum_address(pair_address)
        self.chain = chain
        self.abi = load_abi('uniswap/IUniswapV2Pair.json')
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
    def get_fee(self):
        fee = self.contract.functions.fee().call()
        return  fee