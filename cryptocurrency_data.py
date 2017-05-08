# =============================================================================
#          File: cryptocurrency_data.py
#        Author: Andre Brener
#       Created: 05 May 2017
# Last Modified: 06 May 2017
#   Description: description
# =============================================================================
import json
import time
import pickle

from operator import itemgetter

import requests
import pandas as pd


def get_coin_list():

    coin_list_url = 'https://www.cryptocompare.com/api/data/coinlist/'

    response_text = requests.get(coin_list_url).text

    d = json.loads(response_text)
    data = d['Data']

    coin_list = set([
        val['Name'] for val in data.values()
        if all(kw not in val['Name'] for kw in ['*', ' '])
    ])

    return coin_list


def get_price_one_by_one(coin_list):
    price_dict = {}
    for l in coin_list:
        print(l)
        url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsym=USD'.format(
            l)
        response_text = requests.get(url).text
        d = json.loads(response_text)

        if 'Response' not in d.keys():
            for coin, val in d.items():
                price_dict[coin] = val['USD']
    return price_dict


def get_price_all_together(coin_list):

    coin_list_string = ','.join(coin_list)
    price_now_url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD'.format(
        coin_list_string)

    response_text = requests.get(price_now_url).text
    d = json.loads(response_text)

    price_dict = {}
    for coin, val in d.items():
        price_dict[coin] = val['USD']

    return price_dict


def get_coin_price(coin_list, all_together=True):
    if all_together:
        price_dict = get_price_all_together(coin_list)
    else:
        price_dict = get_price_one_by_one(coin_list)

    price_dict = sorted(price_dict.items(), key=itemgetter(1), reverse=True)

    return price_dict


def save_pickle(price_dict):
    
    prices = []

    for coin, val in price_dict:
        new_val = '  $ {}'.format(val)
        prices.append((coin, new_val))

    with open('prices_data.pkl', 'wb') as f:
        pickle.dump(prices, f)


def get_price_history(coin_list, end_date, days_past, price_type):
    ts = time.mktime(end_date.timetuple())
    df_list = []
    for l in coin_list:
        print(l)
        url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=USD&toTs={}&limit={}'.format(
            l, ts, days_past)
        response_text = requests.get(url).text
        d = json.loads(response_text)

        df = pd.DataFrame(d['Data'])[['time', price_type]]
        df['coin'] = l
        df_list.append(df)
    total_df = pd.concat(df_list)
    total_df = total_df.pivot(
        index='time', columns='coin', values=price_type).reset_index()
    total_df['day'] = pd.to_datetime(total_df['time'], unit='s')
    return total_df


if __name__ == '__main__':
    from datetime import date

    # coin_list = get_coin_list()

    coin_list = ['ETH', 'BTC']
    end_date = date(2017, 4, 1)
    days_past = 7
    price_type = 'close'

    price_dict = get_coin_price(coin_list, True)
    save_pickle(price_dict)

    # df = get_price_history(coin_list, end_date, days_past, price_type)

    # print(df)
