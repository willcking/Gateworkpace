from eth_abi.packed import encode_packed
from web3 import Web3
from wconfig import CONTRACT_ADDRESS

# Python implementation of https://github.com/Uniswap/uniswap-v2-periphery/blob/master/contracts/libraries/UniswapV2Library.sol#L17-L26
# We need "factory_address" and "init_code_hash" configuration to make it work in different environments (Uniswap, Sushiswap etc...)
class HashService:

    @staticmethod
    def for_uniswap():
        return HashService(
            factory_address='0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
            init_code_hash='0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f',
        )

    @staticmethod
    def for_pancake_swap_v1():
        return HashService(
            factory_address='0xBCfCcbde45cE874adCB698cC183deBcF17952812',
            init_code_hash='0xd0d4c4cd0848c93cb4fd1f498d7013ee6bfb25783ea21593d5834f5d250ece66',
        )

    @staticmethod
    def for_pancake_swap():
        return HashService(
            factory_address='0xca143ce32fe78f1f7019d7d551a6402fc5350c73',
            init_code_hash='0x00fb7f630766e6a796048ea87d01acd3068e8ff67d078148a3fa3f4a84f69bd5',
        )

    @staticmethod
    def for_pancaketest_swap():
        return HashService(
            factory_address=CONTRACT_ADDRESS['bsctest']['pancaketest_swap']['factory'],
            init_code_hash='0xecba335299a6693cb2ebc4782e74669b84290b6378ea3a3873c7231a8d7d1074',
        )


    @staticmethod
    def for_joe_swap():
        return HashService(
            factory_address=CONTRACT_ADDRESS['avax']['joe_swap']['factory'],
            init_code_hash='0x0bbca9af0511ad1a1da383135cf3a8d2ac620e549ef9f6ae3a4c33c2fed0af91',
        )

    @staticmethod
    def for_quick_swap():
        return HashService(
            factory_address=CONTRACT_ADDRESS['matic']['quick_swap']['factory'],
            init_code_hash='',
        )

    def __init__(self, factory_address: str, init_code_hash: str):
        self.init_code_hash = init_code_hash
        self.factory_address = factory_address

    def calculate_pair_adress(self, tokenA, tokenB):
        tokenA = Web3.to_checksum_address(tokenA)
        tokenB = Web3.to_checksum_address(tokenB)

        tokenA_hex = bytes.fromhex(tokenA[2:])
        tokenB_hex = bytes.fromhex(tokenB[2:])
        if tokenA_hex < tokenB_hex:
            token0 = tokenA
            token1 = tokenB
        else:
            token1 = tokenA
            token0 = tokenB

        b_salt = Web3.keccak(encode_packed(['address', 'address'], [token0, token1]))

        pre = '0xff'
        b_pre = bytes.fromhex(pre[2:])
        b_address = bytes.fromhex(self.factory_address[2:])
        b_init_code = bytes.fromhex(self.init_code_hash[2:])
        b_result = Web3.keccak(
            encode_packed(['bytes', 'bytes', 'bytes', 'bytes'], [b_pre, b_address, b_salt, b_init_code]))
        result_address = Web3.to_checksum_address(b_result[12:].hex())
        return result_address, token0, token1