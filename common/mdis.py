import time
from datetime import datetime
from typing import (
    Callable,
    Dict,
    Optional,
)

from web3 import Web3
from web3.gas_strategies.time_based import (
    fast_gas_price_strategy,
    medium_gas_price_strategy,
    slow_gas_price_strategy,
    glacial_gas_price_strategy,
)
from web3.types import (
    TxReceipt,
    TxParams,
)

from core.libs import load_abi, log

Wei = int
Ether = float
TokWei = int
Token = float
TxHash = str

GAS_STRATEGY_MAP: Dict[str, Callable] = {
    'fast': fast_gas_price_strategy,  # 1 minute
    'medium': medium_gas_price_strategy,  # 5 minutes
    'slow': slow_gas_price_strategy,  # 1 hour
    'glacial': glacial_gas_price_strategy,  # 24 hours
}

MAX_APPROVAL_HEX: str = '0x' + 'f' * 64
MAX_APPROVAL_INT: int = int(MAX_APPROVAL_HEX, 16)

FACTORY_ADDRESS: str = '0x2F3F03b6a1B1d73b01390E234AE813bc06d5B8e8'
FACTORY_ABI: str = load_abi('mdis/IMdisFactory.json')

ROUTER_ADDRESS: str = '0x40367258BB8b9195446E99079391D7Ccb5AaeaB9'
ROUTER_ABI: str = load_abi('mdis/IMdisRouter02.json')

ERC20_ABI: str = load_abi('mdis/IMdisERC20.json')
PAIR_ABI: str = load_abi('mdis/IMdisPair.json')


class MdisError(Exception):
    pass


class MdisClient:
    def __init__(
            self,
            address: str,
            private_key: str,
            provider: str,
            gas: int,
            gas_price: Wei,
    ) -> None:
        self.address = Web3.to_checksum_address(address)
        self.private_key = private_key
        self.provider = provider

        if self.provider.startswith('https://') or self.provider.startswith("http://"):
            web3_provider = Web3.HTTPProvider(self.provider, request_kwargs={"timeout": 60})
        elif self.provider.startswith('wss://'):
            web3_provider = Web3.WebsocketProvider(self.provider)
        elif self.provider.startswith('/'):
            web3_provider = Web3.IPCProvider(self.provider)
        else:
            raise MdisError(f"Unknown provider type '{self.provider}'")

        self.conn = Web3(web3_provider)
        # if not self.is_connected:
        #     raise MdisError(f"Connection failed to provider '{self.provider}'")

        self.tx_gas = gas
        self.tx_gas_price = gas_price

    #
    # @property
    # def is_connected(self) -> bool:
    #     return self.conn.isConnected()
    #
    #

    def __repr__(self) -> str:
        return f"<MdisClient({self.provider})@{hex(id(self))}>"

    def _get_tx_params(
            self,
            amount: Wei = 0,
            gas: Optional[int] = None,
            gas_price: Optional[Wei] = None,
            nonce: Optional[int] = None,
    ) -> TxParams:
        return {
            'from': self.address,
            'value': amount,
            'gas': gas if gas is not None else self.tx_gas,
            'gasPrice': gas_price if gas_price is not None else self.tx_gas_price,
            'nonce': (
                nonce
                if nonce is not None
                else self.conn.eth.getTransactionCount(self.address)
            ),
        }

    def _submit_tx(self, func: Callable, params: Dict) -> TxHash:
        tx = func.buildTransaction(params)
        tx_signed = self.conn.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.conn.eth.sendRawTransaction(tx_signed.rawTransaction)
        return Web3.toHex(tx_hash)


class TokenPair(MdisClient):
    def __init__(
            self,
            address: str,
            private_key: str,
            provider: str,
            tokenA: str,  # Token address
            tokenB: str,
            max_slippage: float = 0.2,  # Fraction
            gas: int = 2 * 10 ** 4,
            gas_price: Wei = Web3.toWei(1, 'gwei'),
            transaction_timeout: int = 300,  # Seconds
    ) -> None:
        super().__init__(
            address,
            private_key,
            provider,
            gas,
            gas_price,
        )
        self.pair = {
            tokenA: {
                "symbool": "",
                "decimal": ""
            },
            tokenB: {
                "symbol": "",
                "decimal": ""
            }
        }

        self.tokenA = Web3.to_checksum_address(tokenA)
        self.tokenB = Web3.to_checksum_address(tokenB)
        self.max_slippage = max_slippage
        self.tx_timeout = transaction_timeout

        self.contract = self.conn.eth.contract(
            address=Web3.to_checksum_address(FACTORY_ADDRESS),
            abi=FACTORY_ABI
        )
        self.router = self.conn.eth.contract(
            address=Web3.to_checksum_address(ROUTER_ADDRESS),
            abi=ROUTER_ABI
        )

        self.get_token_params(self.pair[tokenA], tokenA)
        self.get_token_params(self.pair[tokenB], tokenB)

    def get_token_params(self, token, token_addr):
        token_contract = self.conn.eth.contract(
            address=Web3.to_checksum_address(token_addr),
            abi=PAIR_ABI
        )
        token['symbol'] = token_contract.functions.symbol().call()
        token['decimal'] = token_contract.functions.decimals().call()
        token['contract'] = self.conn.eth.contract(
            address=Web3.to_checksum_address(token_addr),
            abi=ERC20_ABI
        )

    @property
    def _tx_deadline(self) -> int:
        """ Generate a deadline timestamp for transaction.
        """
        return int(time.time()) + self.tx_timeout

    def _tokwei_price_in_wei(self, amount: TokWei) -> Wei:
        """ Amount of tokens you can expect to get for supplied amount of Wei.
        """
        return self.router.functions.getAmountsIn(
            amount,
            [self.tokenB, self.tokenA]
        ).call()[0]

    def _wei_price_in_tokwei(self, amount: Wei) -> TokWei:
        """ Amount of Wei you can expect to get for supplied amount of tokens.
        """
        return self.router.functions.getAmountsOut(
            amount,
            [self.tokenB, self.tokenA]
        ).call()[-1]

    def _token_to_tokwei(self, token, amount: Token) -> TokWei:
        return TokWei(amount * (10 ** self.pair[token]['decimal']))

    def _tokwei_to_token(self, token, amount: TokWei) -> Token:
        return Token(amount / (10 ** self.pair[token]['decimal']))

    def token_balance(self, token_addr) -> Token:
        """ Pair token balance.
        """
        balance: TokWei = self.pair[token_addr]['contract'].functions.balanceOf(self.address).call()
        return self._tokwei_to_token(token_addr, balance)

    def is_token_approved(
            self,
            amount: TokWei = MAX_APPROVAL_INT,
            token_addr: str = ""
    ) -> bool:
        erc20_contract = self.conn.eth.contract(
            address=token_addr,
            abi=ERC20_ABI
        )

        approved_amount = erc20_contract.functions.allowance(
            token_addr, self.router.address
        ).call()

        return approved_amount >= amount

    def wait(self, hash: TxHash, timeout: int = 3600) -> TxReceipt:
        return self.conn.eth.waitForTransactionReceipt(hash, timeout=timeout)

    def approve_token(
            self,
            token_addr,
            max_approval: TokWei = MAX_APPROVAL_INT,
            gas: Optional[int] = None,
            gas_price: Optional[Wei] = None,
            nonce: Optional[int] = None,
    ) -> None:
        if self.is_token_approved(amount=max_approval, token_addr=token_addr):
            log.debug(
                (
                    " already approved for transfer"
                )
            )
            return

        log.info(
            f"Approving  for transfer"
        )
        log.debug(f"Approval gas: {gas or self.tx_gas}")
        log.debug(f"Approval gas price: {gas_price or self.tx_gas_price} Wei")
        log.debug(f"Approval nonce: {nonce or 'Default'}")

        func = self.pair[token_addr]['contract'].functions.approve(self.router.address, max_approval)
        params = self._get_tx_params(
            gas=gas,
            gas_price=gas_price,
            nonce=nonce,
        )

        # NOTE: Wallet nonce update is lagging behind and is not updated immediately after
        # transaction receipt is received. This causes same nonce to be reused on the next
        # transaction following approval.
        current_nonce = (
            nonce
            if nonce is not None
            else self.conn.eth.getTransactionCount(self.address)
        )
        tx_hash = self._submit_tx(func, params)

        timeout = 3600  # 1 hour
        timer_start = time.monotonic()
        self.wait(tx_hash, timeout)

        # NOTE: Wait for nonce to be incremented of for the timeout interval to run out.
        while (
                current_nonce == self.conn.eth.getTransactionCount(self.address)
                and time.monotonic() - timer_start <= timeout
        ):
            time.sleep(0.5)

        log.info(
            f"The token was approved for transfer"
        )

    def swap_token2token(
            self,
            amount: Token,
            tokenA_addr: str,
            tokenB_addr: str,
            gas: Optional[int] = None,
            gas_price: Optional[Wei] = None,
            nonce: Optional[int] = None,
    ) -> TxHash:
        """ Swap Token to Token.
        """
        unswap_amount: TokWei = self._token_to_tokwei(tokenA_addr, amount)

        amount_out_min: Wei = Wei(
            (1 - self.max_slippage) * self._tokwei_price_in_wei(unswap_amount)
        )
        path = [self.tokenA, self.tokenB]
        to_address = self.address
        deadline = self._tx_deadline

        log.info(
            (
                f"Uswapping {amount} {self.pair[self.tokenA]['symbol']} for a minimum of "
                f"{self._tokwei_to_token(self.tokenB, amount_out_min)} {self.pair[self.tokenB]['symbol']}"
            )
        )
        log.debug(f"Unswap path: {path}")
        log.debug(f"Unswap address: {to_address}")
        log.debug(f"Unswap deadline: {datetime.fromtimestamp(deadline)}")
        log.debug(f"Unswap gas: {gas or self.tx_gas}")
        log.debug(f"Unswap gas price: {gas_price or self.tx_gas_price} Wei")
        log.debug(f"Unswap nonce: {nonce or 'Default'}")

        func = self.router.functions.swapExactTokensForTokens(
            unswap_amount,
            amount_out_min,
            path,
            to_address,
            deadline,
        )
        params = self._get_tx_params(
            gas=gas,
            gas_price=gas_price,
            nonce=nonce,
        )

        return self._submit_tx(func, params)
