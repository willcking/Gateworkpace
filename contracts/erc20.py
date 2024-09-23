from core.contract import Contract
from core.libs import Token, TokenWei, AddressType, MAX_APPROVAL_INT
from core.libs import load_abi


class ERC20Contract(Contract):
    def __init__(self,
                 chain,
                 token_name: str = None,
                 token_addr: str = None,
                 ) -> None:
        if token_name is None:
            self.address = chain.w3.to_checksum_address(token_addr)
        if token_addr is None:
            self.token_name = token_name
            self.address = chain.w3.to_checksum_address(chain.token[token_name])
        self.chain = chain
        self.abi = load_abi('ERC20.json')
        self.contract = chain.w3.eth.contract(
            address=chain.w3.to_checksum_address(self.address),
            abi=self.abi
        )
        #self.token_symbol = self.contract.functions.symbol().call()
        #self.token_decimals = self.contract.functions.decimals().call()

    def token_info(self):
        self.logger.info(
            f'token name {self.token_symbol} \t token decimal {self.token_decimals} \t token addr {self.address}')

    def _token_multiply_decimal(self, amount: Token) -> TokenWei:
        return TokenWei(amount * (10 ** self.token_decimals))

    def _token_devide_decimal(self, amount: TokenWei) -> Token:
        return Token(amount / (10 ** self.token_decimals))

    def token_transfer(self, to_address, value, gas=None):
        if not gas:
            gas = 200000
        to_address = self.chain.w3.to_checksum_address(to_address)
        value=int(value)
        func = self.contract.functions.transfer(to_address, value)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param
    def balance(self, address):
        address = self.chain.w3.to_checksum_address(address)
        return self.contract.functions.balanceOf(address).call()
    def token_transfer_all(self, from_addr, to_address, gas=None):
        from_addr = self.chain.w3.to_checksum_address(from_addr)
        to_address = self.chain.w3.to_checksum_address(to_address)
        value = self.token_balance_wei(from_addr)
        if value == 0:
            self.logger.error("balance is zero")
            return {}
        if not gas:
            gas = 100000
        func = self.contract.functions.transfer(to_address, value)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param

    def token_balance_wei(self, address) -> Token:
        """ Pair token balance.
        """
        address = self.chain.w3.to_checksum_address(address)
        balance: TokenWei = self.contract.functions.balanceOf(address).call()
        self.logger.info(f'Token Balance: {self.token_symbol}: {balance}')
        return balance

    def token_balance(self, address) -> Token:
        """ Pair token balance.
        """
        address = self.chain.w3.to_checksum_address(address)
        balance: TokenWei = self.contract.functions.balanceOf(address).call()
        balance = self._token_devide_decimal(balance)
        self.logger.info(f'Token Balance: {self.token_symbol}: {balance}')
        return balance

    def is_token_approved(
            self,
            from_address: AddressType = None,
            approve_to: AddressType = None,
            amount: TokenWei = MAX_APPROVAL_INT,
    ) -> bool:
        self.logger.info(f'checking approve..')
        approve_to = self.chain.w3.to_checksum_address(approve_to)
        from_address = self.chain.w3.to_checksum_address(from_address)

        erc20_contract = self.chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

        approved_amount = erc20_contract.functions.allowance(
            from_address, approve_to
        ).call()
        self.logger.info(f"approved {approved_amount}, need approved {amount}, enough? {approved_amount >= amount}")
        return approved_amount >= amount

    def approve_token(
            self,
            from_address: AddressType = None,
            approve_to: AddressType = None,
            max_approval: TokenWei = MAX_APPROVAL_INT,
    ) -> None:
        gas = 200000
        approve_to = self.chain.w3.to_checksum_address(approve_to)
        from_address = self.chain.w3.to_checksum_address(from_address)

        if self.is_token_approved(from_address, approve_to, max_approval):
            self.logger.debug(
                (
                    f"The {self._token_devide_decimal(max_approval)} of "
                    f"{self.token_symbol} is already approved for transfer"
                )
            )
            return {}

        self.logger.info(
            (
                f"Approving {self._token_devide_decimal(max_approval)} "
                f"of {self.token_symbol} for transfer"
            )
        )
        # self.logger.debug(f"Approval gas: {gas}")
        # self.logger.debug(f"Approval gas price: {self.chain.gas_price} Wei")
        self.logger.debug(f"Approval amount : {max_approval} Wei")
        erc20_contract = self.chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

        func = erc20_contract.functions.approve(approve_to, max_approval)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param

    def cancle_approve_token(
            self,
            from_address: AddressType = None,
            approve_to: AddressType = None,
    ) -> None:
        gas = 200000
        approve_to = self.chain.w3.to_checksum_address(approve_to)
        from_address = self.chain.w3.to_checksum_address(from_address)

        # self.logger.debug(f"Approval gas: {gas}")
        # self.logger.debug(f"Approval gas price: {self.chain.gas_price} Wei")
        self.logger.debug(f"Cancel approve..")
        erc20_contract = self.chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

        func = erc20_contract.functions.approve(approve_to, 0)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param

