from core.chain_network import ChainNetwork
from core.contract import Contract
from core.libs import AddressType
from core.libs import load_abi


class SwapArbContract(Contract):
    def __init__(self,
                 chain: ChainNetwork,
                 arb_address: AddressType
                 ) -> None:
        self.app_name = 'arbitrage'
        self.address = chain.w3.to_checksum_address(arb_address)
        self.chain = chain
        self.abi = load_abi('arbitrage/ExampleContract.json')
        self.contract = chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def flashswap(self, from_address: AddressType, tokenBorrow, amount, tokenPay, gas: int):
        from_address = self.chain.w3.to_checksum_address(from_address)
        userData = bytes('', encoding='UTF-8')
        func = self.contract.functions.flashSwap(tokenBorrow,
                                                 # borrow_amount,
                                                 amount,
                                                 tokenPay,
                                                 userData)

        tx_param = self._build_tx(func, gas=gas)
        return tx_param
