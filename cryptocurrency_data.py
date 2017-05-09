# =============================================================================
#          File: cryptocurrency_data.py
#        Author: Andre Brener
#       Created: 05 May 2017
# Last Modified: 09 May 2017
#   Description: description
# =============================================================================
import json
import pickle

from operator import itemgetter

import requests


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


if __name__ == '__main__':
    # coin_list = get_coin_list()

    coin_list = ['ETH', 'BTC']

    price_dict = get_coin_price(coin_list, True)
    save_pickle(price_dict)
