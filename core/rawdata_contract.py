import datetime
from datetime import timezone
from web3 import Web3
from contracts.erc20 import ERC20Contract
from core.contract import Contract
from core.libs import Wei, TokenWei, AddressType
from core.libs import load_abi
from typing import (
    Callable,
    Dict,
    Optional,
)


class RawDataContract(Contract):
    def __init__(self,
                 chain,
                 address
                 ) -> None:
        self.address = chain.w3.to_checksum_address(address)
        self.chain = chain
        self.abi = ''
        self.contract = ''


    def send_raw_data(self, data: str = None, gas: int = None):
        if not data:
            data = '0x'
        tx_parm = self._build_diy_tx(to_address=self.address, data=data, gas=gas)
        return tx_parm

    def send_raw_data_value(self, data: str = None, eth_value: TokenWei=0, gas: int = None):
        if not data:
            data = '0x'
        eth_value = int(eth_value)
        tx_param = self._build_diy_tx(to_address=self.address, data=data, gas=gas)
        tx_param['value'] = TokenWei(eth_value)
        return tx_param

    def call_function(self, data = None):
        if not data:
            data = '0x4eea9a8d0000000000000000000000008d88F384fB251C08805944F0C31e52A2277B530b'
        tx_parm = self._build_diy_tx(to_address=self.address, data=data, gas=200000)
        return tx_parm

    """
    https://ethereum.stackexchange.com/questions/73399/how-to-generate-the-full-list-of-function-selectors-for-a-contract
    """
    def calc_selector(self, signature: str = "transfer(address,uint256)"):
        selector = Web3.keccak(text=signature).hex()[:10]
        self.logger.info(f"signature: {signature} : selector {selector}")
        return selector