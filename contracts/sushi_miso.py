from core.chain_network import ChainNetwork
from core.contract import Contract
from core.libs import TokenWei, AddressType
from core.libs import load_abi


class MisoContract(Contract):
    def __init__(self,
                 chain: ChainNetwork,
                 miso_address: AddressType
                 ) -> None:
        self.app_name = 'sushi miso'
        self.address = chain.w3.to_checksum_address(miso_address)
        self.chain = chain
        self.abi = load_abi('sushi_miso.json')
        self.contract = chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def is_Open(self, ) -> list:
        isopen = self.contract.functions.isOpen().call()
        self.logger.info(f"chain: {self.chain.chain_name}  miso addr: {self.address}  status {isopen}")
        return isopen

    def get_paymentCurrency(self):
        currency = self.contract.functions.paymentCurrency().call()
        self.logger.info(f'payment currency : {currency} ')
        return currency

    def commit_Token(self, amount: TokenWei):
        gas = 200000
        # readAndAgreedToMarketParticipationAgreement = True
        func = self.contract.functions.commitTokens(amount, True)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param

    def commit_ETH(self, amount: TokenWei):
        gas = 200000
        func = self.contract.functions.commitETH(amount, 1)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param
