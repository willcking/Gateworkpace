import json
import time
from datetime import datetime

from common.w3client import W3Client
from core.libs import load_abi, get_logger
from wconfig import CONTRACT_ADDRESS

logger = get_logger('pairswap.log')

Wei = int
GWei = int
Ether = float
TokWei = int
Token = float
TxHash = str

from typing import (
    Optional,
    Tuple,
)

from web3 import Web3

from web3.types import (
    TxReceipt,
)

MAX_APPROVAL_HEX: str = '0x' + 'f' * 64
MAX_APPROVAL_INT: int = int(MAX_APPROVAL_HEX, 16)


class ETHPair(W3Client):
    def __init__(
            self,
            address: str,
            private_key: str,
            chain: str,
            token: str,  # Token address
            max_slippage: float = 0.2,  # Fraction
            transaction_timeout: int = 300,  # Seconds
    ) -> None:
        super().__init__(
            address,
            private_key,
            chain,
        )

        self.token = Web3.to_checksum_address(token)
        self.max_slippage = max_slippage
        self.tx_timeout = transaction_timeout
        FACTORY_ADDRESS: str = CONTRACT_ADDRESS[self.chain]['uni']['factory']
        FACTORY_ABI: str = load_abi('IUniswapV2Factory.json')

        ROUTER_ADDRESS: str = CONTRACT_ADDRESS[self.chain]['uni']['router']
        ROUTER_ABI: str = load_abi('IUniswapV2Router02.json')

        ERC20_ABI: str = load_abi('IUniswapV2ERC20.json')
        PAIR_ABI: str = load_abi('IUniswapV2Pair.json')

        self.contract = self.conn.eth.contract(
            address=Web3.to_checksum_address(FACTORY_ADDRESS),
            abi=FACTORY_ABI
        )
        self.router = self.conn.eth.contract(
            address=Web3.to_checksum_address(ROUTER_ADDRESS),
            abi=ROUTER_ABI
        )
        self.token_contract = self.conn.eth.contract(
            address=Web3.to_checksum_address(self.token),
            abi=PAIR_ABI
        )
        self.token_symbol = self.token_contract.functions.symbol().call()
        self.token_decimals = self.token_contract.functions.decimals().call()

    @staticmethod
    def _eth_to_wei(amount: Ether) -> Wei:
        return Wei(Web3.toWei(amount, 'ether'))

    @staticmethod
    def _wei_to_eth(amount: Wei) -> Ether:
        return Ether(Web3.fromWei(amount, 'ether'))

    def _token_to_tokwei(self, amount: Token) -> TokWei:
        return TokWei(amount * (10 ** self.token_decimals))

    def _tokwei_to_token(self, amount: TokWei) -> Token:
        return Token(amount / (10 ** self.token_decimals))

    @property
    def weth_address(self) -> str:
        return self.router.functions.WETH().call()

    @property
    def balance(self) -> Ether:
        """ Pair ETH balance.
        """
        balance: Wei = self.conn.eth.getBalance(self.address)
        return self._wei_to_eth(balance)

    @property
    def token_balance(self) -> Token:
        """ Pair token balance.
        """
        balance: TokWei = self.token_contract.functions.balanceOf(self.address).call()
        return self._tokwei_to_token(balance)

    @property
    def balances(self) -> Tuple[Ether, Token]:
        """ Current pair balance (ETH, Token)
        """
        return (self.balance, self.token_balance)

    def __repr__(self) -> str:
        return f"<ETHPair({self.token_symbol})@{hex(id(self))}>"

    def __str__(self) -> str:
        return json.dumps({'ETH': self.balance, self.token_symbol: self.token_balance})

    def __bool__(self) -> bool:
        return (
                self.is_connected
                and (
                        bool(self.balance)
                        or bool(self.token_balance)
                )
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
            [self.weth_address, self.token]
        ).call()[0]

    def _wei_price_in_tokwei(self, amount: Wei) -> TokWei:
        """ Amount of Wei you can expect to get for supplied amount of tokens.
        """
        return self.router.functions.getAmountsOut(
            amount,
            [self.weth_address, self.token]
        ).call()[-1]

    @property
    def price(self, amount: Ether = 1) -> Token:
        """ Price of ETH in Token.
        """
        return self._tokwei_to_token(
            self._wei_price_in_tokwei(
                self._eth_to_wei(amount)
            )
        )

    @property
    def token_price(self, amount: Token = 1) -> Ether:
        """ Price of Token in ETH.
        """
        return self._wei_to_eth(
            self._tokwei_price_in_wei(
                self._token_to_tokwei(amount)
            )
        )

    def is_token_approved(
            self,
            amount: TokWei = MAX_APPROVAL_INT,
    ) -> bool:
        erc20_contract = self.conn.eth.contract(
            address=self.token,
            abi=PAIR_ABI
        )

        approved_amount = erc20_contract.functions.allowance(
            self.address, self.router.address
        ).call()

        return approved_amount >= amount

    def wait(self, hash: TxHash, timeout: int = 3600) -> TxReceipt:
        return self.conn.eth.waitForTransactionReceipt(hash, timeout=timeout)

    def approve_token(
            self,
            max_approval: TokWei = MAX_APPROVAL_INT,
            gas: Optional[int] = None,
            gas_price: Optional[Wei] = None,
            nonce: Optional[int] = None,
    ) -> None:
        if self.is_token_approved(max_approval):
            logger.debug(
                (
                    f"The {self._tokwei_to_token(max_approval)} of "
                    f"{self.token_symbol} is already approved for transfer"
                )
            )
            return

        logger.info(
            (
                f"Approving {self._tokwei_to_token(max_approval)} "
                f"of {self.token_symbol} for transfer"
            )
        )
        logger.debug(f"Approval gas: {gas or self.tx_gas}")
        logger.debug(f"Approval gas price: {gas_price or self.tx_gas_price} Wei")
        logger.debug(f"Approval nonce: {nonce or 'Default'}")

        erc20_contract = self.conn.eth.contract(
            address=self.token,
            abi=ERC20_ABI
        )

        func = erc20_contract.functions.approve(self.router.address, max_approval)
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

        logger.info(
            (
                f"The {self._tokwei_to_token(max_approval)} of "
                f"{self.token_symbol} was approved for transfer"
            )
        )

    def swap(
            self,
            amount: Ether,
            gas: Optional[int] = None,
            gas_price: Optional[Wei] = None,
            nonce: Optional[int] = None,
    ) -> TxHash:
        """ Swap ETH to Token.
        """
        swap_amount: Wei = self._eth_to_wei(amount)

        amount_out_min: TokWei = TokWei(
            (1 - self.max_slippage) * self._wei_price_in_tokwei(swap_amount)
        )
        path = [self.weth_address, self.token]
        to_address = self.address
        deadline = self._tx_deadline

        logger.info(
            (
                f"Swapping {amount} ETH for a minimum of "
                f"{self._tokwei_to_token(amount_out_min)} {self.token_symbol}"
            )
        )
        logger.debug(f"Swap path: {path}")
        logger.debug(f"Swap address: {to_address}")
        logger.debug(f"Swap deadline: {datetime.fromtimestamp(deadline)}")
        logger.debug(f"Swap gas: {gas or self.tx_gas_price}")
        logger.debug(f"Swap gas price: {gas_price or self.tx_gas} Wei")
        logger.debug(f"Swap nonce: {nonce or 'Default'}")

        func = self.router.functions.swapExactETHForTokens(
            amount_out_min,
            path,
            to_address,
            deadline,
        )
        params = self._get_tx_params(
            amount=swap_amount,
            gas=gas,
            gas_price=gas_price,
            nonce=nonce,
        )

        return self._submit_tx(func, params)

    def unswap(
            self,
            amount: Token,
            gas: Optional[int] = None,
            gas_price: Optional[Wei] = None,
            nonce: Optional[int] = None,
    ) -> TxHash:
        """ Swap Token to ETH.
        """
        unswap_amount: TokWei = self._token_to_tokwei(amount)

        self.approve_token(
            max_approval=unswap_amount,
            gas=gas,
            gas_price=gas_price,
            nonce=nonce,
        )

        amount_out_min: Wei = Wei(
            (1 - self.max_slippage) * self._tokwei_price_in_wei(unswap_amount)
        )
        path = [self.token, self.weth_address]
        to_address = self.address
        deadline = self._tx_deadline

        logger.info(
            (
                f"Unswapping {amount} {self.token_symbol} for a minimum of "
                f"{self._wei_to_eth(amount_out_min)} ETH"
            )
        )
        logger.debug(f"Unswap path: {path}")
        logger.debug(f"Unswap address: {to_address}")
        logger.debug(f"Unswap deadline: {datetime.fromtimestamp(deadline)}")
        logger.debug(f"Unswap gas: {gas or self.tx_gas}")
        logger.debug(f"Unswap gas price: {gas_price or self.tx_gas_price} Wei")
        logger.debug(f"Unswap nonce: {nonce or 'Default'}")

        func = self.router.functions.swapExactTokensForETH(
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
