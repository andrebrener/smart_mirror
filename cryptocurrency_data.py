# =============================================================================
#          File: cryptocurrency_data.py
#        Author: Andre Brener
#       Created: 05 May 2017
# Last Modified: 27 May 2017
#   Description: description
# =============================================================================
import os
import json
import pickle
import logging
import logging.config

from operator import itemgetter

import requests

from config import config, PROJECT_DIR

os.chdir(PROJECT_DIR)

logger = logging.getLogger('main_logger')


def get_prices(coin_list):

    coin_list_string = ','.join(coin_list)
    price_now_url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD'.format(
        coin_list_string)

    try:
        response_text = requests.get(price_now_url).text
        logger.info("Got Coin Data")

    except Exception as e:
        logger.error(str(e))
        raise

    d = json.loads(response_text)

    price_dict = {}
    for coin, val in d.items():
        price_dict[coin] = val['USD']

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
    logging.config.dictConfig(config['logger'])

    coin_list = ['ETH', 'BTC']

    price_dict = get_prices(coin_list)
    save_pickle(price_dict)
