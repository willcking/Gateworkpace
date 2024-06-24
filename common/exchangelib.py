# coding: utf-8
import requests
import csv
import threading, queue, time
from concurrent.futures import ThreadPoolExecutor
import datetime

PRICE_DATA = queue.Queue(maxsize=50)

def get_gate_price(pair):

    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/spot/order_book'
    query_param = f'currency_pair={pair}'
    r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    data = r.json()
    print(data)
    return float(data['asks'][0][0])

