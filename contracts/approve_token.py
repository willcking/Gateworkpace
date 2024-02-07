from contracts.eggswap import EggSwapContract
from contracts.erc20 import ERC20Contract
from core.chain_account import ChainAccount
from core.chain_network import ChainNetwork

def approve_to_addr(chain_name, token_name, approve_to, my_account):
    current_chain = ChainNetwork(chain_name)
    my_chain_account = ChainAccount(my_account, current_chain)

    raca_contract = ERC20Contract(token_name=token_name, chain=current_chain)
    tx_params  = raca_contract.approve_token(from_address=my_account.address,  approve_to=approve_to)
    if tx_params == {}:
        return
    my_chain_account.sign_and_push(tx_params)


def cancle_approve_to_addr(chain_name, token_name, approve_to, my_account):
    current_chain = ChainNetwork(chain_name)
    my_chain_account = ChainAccount(my_account, current_chain)

    raca_contract = ERC20Contract(token_name=token_name, chain=current_chain)
    tx_params  = raca_contract.cancle_approve_token(from_address=my_account.address,  approve_to=approve_to)
    if tx_params == {}:
        return
    my_chain_account.sign_and_push(tx_params)
