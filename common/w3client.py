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

from core.libs import get_logger
from wconfig import CHAIN_PROVIDER

Wei = int
GWei = int
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

logger = get_logger('flashswap.log')


class W3ClientError(Exception):
    pass


class W3Client:
    def __init__(
            self,
            address: str,
            private_key: str,
            chain: str,
    ) -> None:
        self.address = Web3.to_checksum_address(address)
        self.private_key = private_key
        self.chain = chain
        self.provider = CHAIN_PROVIDER[self.chain]

        if self.provider.startswith('https://') or self.provider.startswith('http://'):
            web3_provider = Web3.HTTPProvider(self.provider, request_kwargs={"timeout": 60})
        elif self.provider.startswith('wss://'):
            web3_provider = Web3.WebsocketProvider(self.provider)
        elif self.provider.startswith('/'):
            web3_provider = Web3.IPCProvider(self.provider)
        else:
            raise (f"Unknown provider type '{self.provider}'")

        self.conn = Web3(web3_provider)

        # self.tx_gas = gas
        # self.tx_gas_price = gas_price

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

    def wait(self, hash: TxHash, timeout: int = 3600) -> TxReceipt:
        return self.conn.eth.waitForTransactionReceipt(hash, timeout=timeout)

    @property
    def is_connected(self) -> bool:
        return self.conn.isConnected()

    def suggest_gas_price(self, mode: str = 'medium') -> Wei:
        """
        Suggests gas price depending on required transaction priority.
        Supported priorities are: 'fast', 'medium', 'slow', 'glacial'.

        Warning: This operation is very slow (~30sec)!
        """

        if mode not in GAS_STRATEGY_MAP:
            raise W3ClientError(
                f"Unsupported gas strategy type, pick from: {[k for k in GAS_STRATEGY_MAP]}"
            )

        self.conn.eth.setGasPriceStrategy(GAS_STRATEGY_MAP[mode])
        return self.conn.eth.generateGasPrice()
