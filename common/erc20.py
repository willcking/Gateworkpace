from web3 import Web3
from web3.types import (
    TxReceipt,
)

from common import orm
from core.libs import load_abi
from wconfig import CHAIN_PROVIDER

TxHash = int

MAX_APPROVAL_HEX: str = '0x' + 'f' * 64
MAX_APPROVAL_INT: int = int(MAX_APPROVAL_HEX, 16)

ERC20_ABI: str = load_abi('ERC20.json')


class ERC20Contract():
    def __init__(
            self,
            chain: str,
            contract_addr: str,
            db_conn
    ) -> None:
        self.chain = chain
        self.provider = CHAIN_PROVIDER[chain]

        if self.provider.startswith('http'):
            web3_provider = Web3.HTTPProvider(self.provider, request_kwargs={"timeout": 60})
        elif self.provider.startswith('wss://'):
            web3_provider = Web3.WebsocketProvider(self.provider)
        elif self.provider.startswith('/'):
            web3_provider = Web3.IPCProvider(self.provider)
        else:
            raise (f"Unknown provider type '{self.provider}'")
        self.conn = Web3(web3_provider)
        self.db_conn = db_conn
        self.contract_addr = contract_addr
        self.arb_contract = self.conn.eth.contract(
            address=Web3.to_checksum_address(self.contract_addr),
            abi=ERC20_ABI
        )

        self.token_decimals = self.get_token_decimal_from_db()
        self.token_symbol = self.get_token_symbol_from_db()

    def get_token_symbol_from_db(self):
        cursor = self.db_conn.cursor()
        sql = "SELECT symbol FROM token WHERE network = %s AND address = %s"
        cursor.execute(sql, (self.chain, self.contract_addr))
        result = cursor.fetchone()
        if result:
            return result[0]

    def get_token_decimal_from_db(self):
        cursor = self.db_conn.cursor()
        sql = "SELECT decimal FROM token WHERE network = %s AND address = %s"
        cursor.execute(sql, (self.chain, self.contract_addr))
        result = cursor.fetchone()
        if result:
            return int(result[0])

    def balance(self, token_addr):
        # print()
        ba = self.arb_contract.functions.balanceOf(
            token_addr
        ).call()
        balance = round(ba / 10 ** self.token_decimals, 8)
        return balance

    def token_balance(self, token_addr: str):
        pass

    def wait(self, hash: TxHash, timeout: int = 3600) -> TxReceipt:
        return self.conn.eth.waitForTransactionReceipt(hash, timeout=timeout)


if __name__ == '__main__':
    pass
