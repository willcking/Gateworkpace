import requests
import json
import os
from core.chain_network import ChainNetworkNew
from contracts.V3swap_quoter import V3SwapQuote
from core.libs import get_logger
from web3.exceptions import ContractLogicError
from wconfig import LOG_PATH
logger = get_logger('chainlist.log')


# 将节点列表写入配置文件
def write_nodes_to_config(nodes, chanid):
    fpath = os.path.join(LOG_PATH, str(chanid)+'config.json')
    with open(fpath, 'w') as f:
        json.dump(nodes, f)

# 从配置文件读取节点列表
def read_nodes_from_config(chanid):

    fpath = os.path.join(LOG_PATH, str(chanid)+'config.json')
    if not os.path.exists(fpath):
        update_chains(1)
    with open(fpath, 'r') as f:
        nodes = json.load(f)
    return nodes




def update_chains(chainid):


    burp0_url = f"https://chainlist.org/_next/data/oL6-l_PHsTNZz4VY3X57d/chain/{chainid}.json?chain={chainid}"
    burp0_headers = {"Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
                     "Purpose": "prefetch", "X-Nextjs-Data": "1", "Sec-Ch-Ua-Mobile": "?0",
                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                     "Sec-Ch-Ua-Platform": "\"macOS\"", "Accept": "*/*", "Sec-Fetch-Site": "same-origin",
                     "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://chainlist.org/",
                     "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
    req = requests.get(burp0_url, headers=burp0_headers)
    rpclst = req.json()["pageProps"]["chain"]["rpc"]

    httprpclst = []
    for i in rpclst:
        if i['url'].startswith('http'):
            chain = ChainNetworkNew(chain_name='eth', provider=i['url'])
            quote_contract = V3SwapQuote(app_name='univ3', chain=chain)

            amount_in = 1000 * 10 ** 18
            base_token = '0x6DEA81C8171D0bA574754EF6F8b412F2Ed88c54D'
            quote_token =  '0xD1D5A4c0eA98971894772Dcd6D2f1dc71083C44E'
            fee = 3000
            try:
                amount_out = quote_contract.quoteExactInputSingle(base_token, quote_token, amount_in, fee)

                if amount_out:

                    httprpclst.append(i[
                    'url' ])
            except ContractLogicError as e:
                logger.info(i['url'])
                httprpclst.append(i[
                                      'url'])
            except Exception as e:

                logger.error(i['url'])
                #logger.error(ExceptionGroup)
                logger.error(e)
                continue

    #print(rpclst, req.status_code)
    logger.info(str(httprpclst))
    write_nodes_to_config(httprpclst, chainid)

if __name__ == '__main__':

    # 从配置文件中读取节点列表
    read_nodes = read_nodes_from_config()
    print("读取的节点列表：", read_nodes)

    write_nodes_to_config(['ddddd'])
    update_chains(1)
