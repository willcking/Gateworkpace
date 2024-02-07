import datetime
from datetime import timezone

from core.chain_network import ChainNetwork
from core.contract import Contract
from core.libs import AddressType, TokenWei
from core.libs import load_abi
from wconfig import CONTRACT_ADDRESS


class SwapRouterContract(Contract):
    def __init__(self,
                 app_name: str,
                 chain: ChainNetwork
                 ) -> None:
        self.app_name = app_name
        self.address = chain.w3.to_checksum_address(CONTRACT_ADDRESS[chain.chain_name][app_name]['router'])
        self.chain = chain
        self.abi = load_abi('uniswap/IUniswapV2Router02.json')
        self.contract = chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def addliquidity(self, ):
        token0 = self.contract.functions.token0().call()
        token1 = self.contract.functions.token1().call()
        return (token0, token1)

    def get_reserve_from_pair(self, ):
        self.logger.debug(f'updating reserve : {self.address}')

        (amount0, amount1, x) = self.contract.functions.getReserves().call()
        return (amount0, amount1)

    def swapExactETHForTokens(self, from_address: AddressType, amountIn: int, amountOuntMin: int, path: []):
        gas = 900000
        dt = datetime.datetime.utcnow()
        utc_time = dt.replace(tzinfo=timezone.utc)
        expired_timestamp = int(utc_time.timestamp()) + 60 * 60

        self.logger.info(f'swap path {path}')
        func = self.contract.functions.swapExactETHForTokens(amountOutMin=amountOuntMin,
                                                                path=path, to=from_address, deadline=expired_timestamp)

        tx_param = self._build_tx(func, gas=gas)
        tx_param['value'] = amountIn
        return tx_param

    def swapExactETHForTokensSupportingFeeOnTransferTokens(self, from_address: AddressType, amountIn: int, amountOuntMin: int, path: []):
        gas = 500000
        dt = datetime.datetime.utcnow()
        utc_time = dt.replace(tzinfo=timezone.utc)
        expired_timestamp = int(utc_time.timestamp()) + 60 * 60

        self.logger.info(f'swap path {path}')
        func = self.contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(amountOutMin=amountOuntMin,
                                                                path=path, to=from_address, deadline=expired_timestamp)

        tx_param = self._build_tx(func, gas=gas)
        tx_param['value'] = amountIn
        return tx_param


    def swapExactAVAXForTokens(self, from_address: AddressType, amountIn: int, amountOuntMin: int, path: []):
        gas = 900000
        dt = datetime.datetime.utcnow()
        utc_time = dt.replace(tzinfo=timezone.utc)
        expired_timestamp = int(utc_time.timestamp()) + 60 * 60

        self.logger.info(f'swap path {path}')
        func = self.contract.functions.swapExactAVAXForTokens(amountOutMin=amountOuntMin,
                                                                path=path, to=from_address, deadline=expired_timestamp)

        tx_param = self._build_tx(func, gas=gas)
        tx_param['value'] = amountIn
        return tx_param

    def swapExactAVAXForTokensSupportingFeeOnTransferTokens(self, from_address: AddressType, amountIn: int, amountOuntMin: int, path: []):
        gas = 500000
        dt = datetime.datetime.utcnow()
        utc_time = dt.replace(tzinfo=timezone.utc)
        expired_timestamp = int(utc_time.timestamp()) + 60 * 60

        self.logger.info(f'swap path {path}')
        func = self.contract.functions.swapExactAVAXForTokensSupportingFeeOnTransferTokens(amountOutMin=amountOuntMin,
                                                                path=path, to=from_address, deadline=expired_timestamp)

        tx_param = self._build_tx(func, gas=gas)
        tx_param['value'] = amountIn
        return tx_param


    def swapExactTokensForTokens(self, from_address: AddressType, amountIn: int, amountOuntMin: int, path: []):
        gas = 900000
        dt = datetime.datetime.utcnow()
        utc_time = dt.replace(tzinfo=timezone.utc)
        expired_timestamp = int(utc_time.timestamp()) + 60 * 60

        self.logger.info(f'swap path {path}')
        func = self.contract.functions.swapExactTokensForTokens(amountIn=amountIn, amountOutMin=amountOuntMin,
                                                                path=path, to=from_address, deadline=expired_timestamp)

        tx_param = self._build_tx(func, gas=gas)
        return tx_param

    def swapExactTokensForTokensSupportingFeeOnTransferTokens(self, from_address: AddressType, amountIn: int, amountOuntMin: int, path: []):
        gas = 900000
        dt = datetime.datetime.utcnow()
        utc_time = dt.replace(tzinfo=timezone.utc)
        expired_timestamp = int(utc_time.timestamp()) + 60 * 60

        self.logger.info(f'swap path {path}')
        func = self.contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(amountIn=amountIn, amountOutMin=amountOuntMin,
                                                                path=path, to=from_address, deadline=expired_timestamp)

        tx_param = self._build_tx(func, gas=gas)
        return tx_param

    def swapETHForExactTokens(self, from_address: AddressType, amountIn: int, amountOuntMin: int, path: []):
        gas = 900000
        dt = datetime.datetime.utcnow()
        utc_time = dt.replace(tzinfo=timezone.utc)
        expired_timestamp = int(utc_time.timestamp()) + 60 * 60

        self.logger.info(f'swap path {path}')
        func = self.contract.functions.swapETHForExactTokens(amountOuntMin,path, from_address, expired_timestamp)

        tx_param = self._build_tx(func, gas=gas)
        tx_param['value'] = amountIn
        return tx_param


    def add_liquidity(
            self,
            from_address: AddressType,
            token_addr_0: AddressType,
            token_addr_1: AddressType,
            amountADesired: TokenWei,
            amountBDesired: TokenWei,
            amountAmin: TokenWei,
            amountBmin: TokenWei
    ) -> str:
        gas = 1500000
        dt = datetime.datetime.utcnow()
        utc_time = dt.replace(tzinfo=timezone.utc)
        expired_timestamp = int(utc_time.timestamp()) + 60 * 60


        token_addr_0 = self.chain.w3.to_checksum_address(token_addr_0)
        token_addr_1 = self.chain.w3.to_checksum_address(token_addr_1)
        self.logger.info(f'add liqudity {token_addr_0} {token_addr_1}')
        func = self.contract.functions.addLiquidity(token_addr_0, token_addr_1, amountADesired, amountBDesired, amountAmin, amountBmin,from_address,  expired_timestamp)

        tx_param = self._build_tx(func, gas=gas)

        return tx_param

    def add_liquidityETH(
            self,
            from_address: AddressType,
            token_addr_0: AddressType,
            amountADesired: TokenWei,
            amountAmin: TokenWei,
            amountETHmin: TokenWei
    ) -> str:
        gas = 1500000
        dt = datetime.datetime.utcnow()
        utc_time = dt.replace(tzinfo=timezone.utc)
        expired_timestamp = int(utc_time.timestamp()) + 60 * 60


        token_addr_0 = self.chain.w3.to_checksum_address(token_addr_0)
        self.logger.info(f'add liqudity {token_addr_0} ETH')
        func = self.contract.functions.addLiquidityETH(token_addr_0, amountADesired, amountAmin, amountETHmin, from_address,  expired_timestamp)

        tx_param = self._build_tx(func, gas=gas)
        tx_param['value'] = amountETHmin
        return tx_param
