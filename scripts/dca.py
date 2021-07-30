#!/usr/bin/env python

import python_bitbankcc
from math import floor
from datetime import datetime
import pathlib
import csv
from settings import BITBANK_API_KEY, BITBANK_API_SECRET


class BitBankPubAPI:
    def __init__(self):
        self.pub = python_bitbankcc.public()

    def get_ticker(self, pair):
        try:
            value = self.pub.get_ticker(pair)
            return value
        except Exception as e:
            print(e)
            return None


class BitBankPrvAPI:
    def __init__(self):
        api_key = BITBANK_API_KEY
        api_secret = BITBANK_API_SECRET
        self.prv = python_bitbankcc.private(api_key, api_secret)

    def get_asset(self):
        try:
            value = self.prv.get_asset()
            return value
        except Exception as e:
            print(e)
            return None

    def buy_order(self, order_price, amount):
        try:
            value = self.prv.order('btc_jpy', order_price, amount, 'buy', 'limit')
            return value
        except Exception as e:
            print(e)
            return None


def main():
    unit = 5000  # unit of rounding order
    dca_amount = 3000  # jpy to buy for each day
    log_file_path = pathlib.Path.home() / 'Devel/bitbank-dca/log.csv'  # log file path
    pub_set = BitBankPubAPI()
    prv_set = BitBankPrvAPI()

    ticker = pub_set.get_ticker('btc_jpy')
    last_price = int(ticker['last'])
    if last_price % unit == 0:
        order_price = last_price-2000
    else:
        order_price = unit * (last_price // unit)
    # find amount closest to dca amount on the 4th decimal
    amount = dca_amount / order_price
    amount = floor(amount * 10 ** 4 + 0.5) / 10 ** 4
    t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    if log_file_path.exists():
        with open(log_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([t, str(order_price), str(amount), str(last_price)])
    else:
        log_file_path.touch()
        with open(log_file_path, 'w+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'order_price', 'amount', 'current_price'])
            writer.writerow([t, str(order_price), str(amount), str(last_price)])

    prv_set.buy_order(order_price=str(order_price), amount=str(amount))


if __name__ == '__main__':
    main()
