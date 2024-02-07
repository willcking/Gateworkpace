import datetime
from datetime import timezone

from core.chain_network import ChainNetwork
from core.contract import Contract
from core.libs import AddressType, TokenWei, Token
from core.libs import load_abi
from core.HashService import HashService
from wconfig import CONTRACT_ADDRESS


class SwapFactoryContract(Contract):
    def __init__(self,
                 app_name: str,
                 chain: ChainNetwork
                 ) -> None:
        self.app_name = app_name
        # factory address
        self.address = chain.w3.to_checksum_address(CONTRACT_ADDRESS[chain.chain_name][app_name]['factory'])
        self.chain = chain
        self.abi = load_abi('uniswap/IUniswapV2Factory.json')
        self.contract = chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def get_pair_length(
            self
    ) -> int:
        func = self.contract.functions.allPairsLength()
        return func.call()

    def get_pair_addr_using_index(
            self,
            pair_index: int
    ) -> str:
        func = self.contract.functions.allPairs(pair_index)
        return func.call()

    def get_pair_addr_using_tokens(
            self,
            token_addr_0: AddressType,
            token_addr_1: AddressType
    ) -> str:
        token_addr_0 = self.chain.w3.to_checksum_address(token_addr_0)
        token_addr_1 = self.chain.w3.to_checksum_address(token_addr_1)
        pair_addr = self.contract.functions.getPair(token_addr_0, token_addr_1).call()
        self.logger.info(f'pair address from factory: {pair_addr}')
        return  pair_addr

    def get_pair_addr_using_tokens_local(
            self,
            token_addr_0: AddressType,
            token_addr_1: AddressType
    ) -> str:
        pair = '0x0000000000000000000000000000000000000000'
        if self.app_name == 'pancake_swap':
            pair = HashService.for_pancake_swap().calculate_pair_adress(
                tokenA=token_addr_0,
                tokenB=token_addr_1
            )[0]
        if self.app_name == 'joe_swap':
            pair = HashService.for_joe_swap().calculate_pair_adress(
                tokenA=token_addr_0,
                tokenB=token_addr_1
            )[0]
        if self.app_name == 'pancaketest_swap':
            pair = HashService.for_pancaketest_swap().calculate_pair_adress(
                tokenA=token_addr_0,
                tokenB=token_addr_1
            )[0]
        self.logger.info(f'calc pair: {pair}')
        return pair

    def create_pair(
            self,
            token_addr_0: AddressType,
            token_addr_1: AddressType
    ) -> str:
        gas = 6008939

        token_addr_0 = self.chain.w3.to_checksum_address(token_addr_0)
        token_addr_1 = self.chain.w3.to_checksum_address(token_addr_1)
        func = self.contract.functions.createPair(token_addr_0, token_addr_1)

        tx_param = self._build_tx(func, gas=gas)

        return tx_param

