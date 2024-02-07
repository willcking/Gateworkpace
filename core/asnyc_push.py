from wconfig import CHAIN_PROVIDER, CONTRACT_ADDRESS, CHAIN_ID, GAS_PRICE
import asyncio

from web3 import Web3
from web3.eth import AsyncEth



async def build_async_w3_http(endpoint_uri: str) -> Web3:
    _web3 = Web3(
        Web3.AsyncHTTPProvider(endpoint_uri),  # type: ignore
        middlewares=[],
        modules={'eth': (AsyncEth,)},
    )
    return _web3


def handle_exception(loop, context):
    print(context['exception'])
    pass

class AsnycChainPool():
    def __init__(self,
                 chain_name: str = None,
                 ) -> None:
        self.chain_name = chain_name
        self.w3_list = []
        self.tasks = []

        for priovider in CHAIN_PROVIDER[self.chain_name+'_pool']:
            w3 = Web3(Web3.AsyncHTTPProvider(priovider), modules={'eth': (AsyncEth,)}, middlewares='')
            self.w3_list.append(w3)



    def push(self, tx_signed):
        if tx_signed:
            for w3 in self.w3_list:
                hex_tx = w3.eth.send_raw_transaction(tx_signed.rawTransaction)
                self.tasks.append(hex_tx)

            loop = asyncio.get_event_loop()
            loop.set_exception_handler(handle_exception)
            #print(dir(loop))
            #help(loop.run_until_complete)
            res = loop.run_until_complete(asyncio.wait(self.tasks))
            #print(len(res))
            for data in res:
                #print("list:"+ str(list(data)))
                #print(list(data))
                if len(data) < 1:
                    continue
                for taskres in data:
                    #print("list:"+ str(list(data)))
                    #print("result:" + str(taskres._result))
                    if taskres._result is None:
                        continue
                    print("hash:" + Web3.toHex(taskres._result))

