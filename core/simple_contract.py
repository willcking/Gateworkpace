import datetime
from datetime import timezone
from web3 import Web3
from contracts.erc20 import ERC20Contract
from core.libs import TokenWei, Token
from core.contract import Contract
from core.libs import Wei, TokenWei, AddressType
import json
from typing import (
    Callable,
    Dict,
    Optional,
)


class SimpleContract(Contract):
    def __init__(self,
                 chain,
                 address: AddressType,
                 abi: list
                 ) -> None:
        self.address = chain.w3.to_checksum_address(address)
        self.chain = chain
        self.abi = json.loads(abi)
        self.contract = chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def write_func(self, func_name: str = None, arg_tuple: list = None, gas: int = None):
        self.logger.info(f'call function name: {func_name}')
        self.logger.info(f'args: {arg_tuple}')
        myfun = getattr(self.contract.functions, func_name)
        if arg_tuple is None:
            func = myfun()
        else:
            func = myfun(arg_tuple)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param
        #

    def write_func_eth(self, func_name: str = None, arg_tuple: tuple = (), eth_value: TokenWei =0, gas: int = None):
        self.logger.info(f'call function name: {func_name}')
        self.logger.info(f'args: {arg_tuple}')
        myfun = getattr(self.contract.functions, func_name)
        if arg_tuple is None:
            myfun = myfun()
        # 1 arg, [arg]
        if len(arg_tuple) == 1:
            myfun = myfun(arg_tuple[0])
        else:
            myfun.args = arg_tuple
            myfun.arguments = arg_tuple
            myfun.kwargs = {}
        tx_param = self._build_tx(myfun, gas=gas)
        tx_param['value'] = TokenWei(eth_value)
        return tx_param
        #


    def read_func(self, func_name: str = None) :
        self.logger.info(f'call function name: {func_name}')
        myfun = getattr(self.contract.functions, func_name)
        res = myfun().call()
        return not res