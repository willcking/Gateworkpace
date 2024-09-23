import json
import logging
import os
import sys
from logging import handlers
import time
from wconfig import LOG_PATH, LOG_LEVEL

Wei = int
GWei = int
Ether = float
TokenWei = int
Token = float
TxHash = str
AddressType = str

EmptyAddress = '0x0000000000000000000000000000000000000000'

MAX_APPROVAL_HEX: str = '0x' + 'f' * 64
MAX_APPROVAL_INT: int = int('0x' + 'f' * 64, 16)


def load_abi(file_name: str) -> str:
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../assets',
        file_name
    )
    with open(file_path) as f:
        return json.load(f)

def get_logger(name):
    logger = logging.getLogger(name)
    fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    fpath = os.path.join(LOG_PATH, name)
    logger.setLevel(LOG_LEVEL)
    if not logger.handlers:
        # Prevent logging from propagating to the root logger
        logger.propagate = 0
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(fmt)
        console.setFormatter(formatter)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        maxBytes = 500 * 1024 * 1024  # 2M
        backupCount = 2  # 最多保留10个文件
        rotating_file_handler = logging.handlers.RotatingFileHandler(
            filename=fpath,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding='utf-8'
        )
        rotating_file_handler.setFormatter(format_str)
        logger.addHandler(rotating_file_handler)
    return logger


class PairswapError(Exception):
    pass


def wait_key_press():
    inp = input("Press 'y' to continue...")
    if inp == 'y':
        pass
    else:
        sys.exit()

def send_signal(gas_price = 1, filename='signal.txt'):
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f'../{filename}'
    )
    signal = open(file_path, 'w')
    signal.write(f'{gas_price}')
    signal.close()

def init_signal(filename='signal.txt'):
    print('set signal empty')
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f'../{filename}'
    )
    signal = open(file_path, 'w')
    signal.close()

def read_signal(filename='signal.txt'):
    print('waitting signal')
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f'../{filename}'
    )
    thefile = open(file_path, "r")

    while True:
        line = thefile.readline(10)
        if not line:
            continue
        break

    return int(line)

def read_signal_json(filename='signal.txt'):
    print('waitting signal')
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f'../{filename}'
    )
    thefile = open(file_path, "r")

    while True:
        line = thefile.readline(200)
        if not line:
            continue
        break

    return eval(line)





def format_blocknative_chainname(chain_name):
    if chain_name == 'bsc':
        return 'bsc-main'
    if chain_name == 'eth':
        return 'main'
    if chain_name == 'ropsten':
        return 'ropsten'
    if chain_name == 'kovan':
        return 'kovan'
    if chain_name == 'matic':
        return 'matic-main'
    else:
        print('wrong chainnet')
        return None

def generate_tokenids(start, end):
    l = []
    for i in range(start, end):
        l.append(str(i))
    return l
