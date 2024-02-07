from core.chain_account import ChainAccount
from core.chain_network import ChainNetwork
from contracts.swap_router import SwapRouterContract
from contracts.erc20 import ERC20Contract


def get_chainname(swap_name):
    chain_name = None
    if swap_name in ['pancake_swap', 'ape_swap']:
        chain_name = 'bsc'
    if swap_name in ['quick_swap']:
        chain_name = 'matic'
    if swap_name in ['goswap']:
        chain_name = 'kovan'
    if swap_name in ['joe_swap']:
        chain_name = 'avax'
    if swap_name in ['spirit_swap']:
        chain_name = 'ftm'
    if swap_name in ['unikovan_swap']:
        chain_name = 'kovan'
    return chain_name

def get_params(swap_name, my_account, tokenIn: str, tokenOut, amountIn, amountOutMin, fee = False):
    chain_name = get_chainname(swap_name)

    print(f'using address: {my_account.address}')
    chain = ChainNetwork(chain_name)
    chain_account = ChainAccount(my_account, chain)

    # if pair_addr == '0x0000000000000000000000000000000000000000':
    #     return []

    if tokenIn.startswith('0x'):
        tokenIn_contract = ERC20Contract(token_addr=tokenIn, chain=chain)
    else:
        tokenIn_contract = ERC20Contract(token_name=tokenIn, chain=chain)

    if tokenOut.startswith('0x'):
        tokenOut_contract = ERC20Contract(token_addr=tokenOut, chain=chain)
    else:
        tokenOut_contract = ERC20Contract(token_name=tokenOut, chain=chain)

    swap_router = SwapRouterContract(app_name=swap_name, chain=chain)
    path = [tokenIn_contract.address, tokenOut_contract.address]
    amountInWei = int(amountIn * 10 ** tokenIn_contract.token_decimals)
    amountOutMinWei = int(amountOutMin * 10 ** tokenOut_contract.token_decimals)

    tx_params = {}

    if (chain_name == 'avax' and tokenIn == 'wavax'):
        if fee:
            tx_params = swap_router.swapExactAVAXForTokensSupportingFeeOnTransferTokens(from_address=my_account.address,
                                                                                       amountIn=amountInWei,
                                                                                       amountOuntMin=amountOutMinWei,
                                                                                       path=path)
        else:
            tx_params = swap_router.swapExactAVAXForTokens(from_address=my_account.address, amountIn=amountInWei,
                                                          amountOuntMin=amountOutMinWei, path=path)
        return tx_params

    if tokenIn in ['wbnb', 'wmatic', 'wftm']:
        if fee:
            tx_params = swap_router.swapExactETHForTokensSupportingFeeOnTransferTokens(from_address=my_account.address,
                                                                                       amountIn=amountInWei,
                                                                                       amountOuntMin=amountOutMinWei,
                                                                                       path=path)
        else:
            tx_params = swap_router.swapExactETHForTokens(from_address=my_account.address, amountIn=amountInWei,
                                                          amountOuntMin=amountOutMinWei, path=path)
        return tx_params
    else:
        if fee:
            tx_params = swap_router.swapExactTokensForTokensSupportingFeeOnTransferTokens(from_address=my_account.address, amountIn=amountInWei,
                                                             amountOuntMin=amountOutMinWei, path=path)

        else:
            tx_params = swap_router.swapExactTokensForTokens(from_address=my_account.address,
                                                                                          amountIn=amountInWei,
                                                                                          amountOuntMin=amountOutMinWei,
                                                                                          path=path)


    #print(tx_params)
    return tx_params, tokenIn_contract, chain_account




def get_liqudity_params(swap_name, my_account, tokenA, tokenB, amountA, amountB):
    chain_name = get_chainname(swap_name)
    chain = ChainNetwork(chain_name)

    factory = SwapRouterContract(app_name=swap_name, chain=chain)

    tokenA_contract = ERC20Contract(token_name=tokenA, chain=chain)
    tokenB_contract = ERC20Contract(token_name=tokenB, chain=chain)

    amountADesired = int(amountA * 10 ** tokenA_contract.token_decimals)
    amountBDesired = int(amountB * 10 ** tokenB_contract.token_decimals)

    return factory.add_liquidity(token_addr_0=tokenA_contract.address,
                                 token_addr_1=tokenB_contract.address,
                                 amountADesired=amountADesired,
                                 amountBDesired=amountBDesired,
                                 amountAmin=int(amountADesired),
                                 from_address=chain.w3.to_checksum_address(my_account.address),
                                 amountBmin=int(amountBDesired * 0.5)
                                 )


def get_ethliqudity_params(swap_name, my_account, token, amount, amountETHmin):
    chain_name = get_chainname(swap_name)
    chain = ChainNetwork(chain_name)

    factory = SwapRouterContract(app_name=swap_name, chain=chain)

    tokenA_contract = ERC20Contract(token_name=token, chain=chain)
    amountADesired = int(amount * 10 ** tokenA_contract.token_decimals)
    amountETHmin = int(amountETHmin * 10 ** tokenA_contract.token_decimals)

    return factory.add_liquidityETH(token_addr_0=tokenA_contract.address,
                                 amountADesired=amountADesired,
                                 amountAmin=int(amountADesired),
                                 from_address=chain.w3.to_checksum_address(my_account.address),
                                 amountETHmin=int(amountETHmin * 0.5)
                                 )
