import time

import schedule
from pymongo import MongoClient

from cpchain_test.config import cfg

EVERYDAY = 1000
FAUCET_VALUE = 1
LIMIT_COIN = 10
DAY_SECENDS = 60 * 60 * 24

mongo = cfg['db']['ip']
CLIENT = MongoClient(host=mongo, port=27017)
faucet_collection = CLIENT['cpchain']['faucet']


def coin_update():
    faucet_collection.update({}, {"$set": {"coins_daily": EVERYDAY}}, True)


schedule.every().day.do(coin_update)

if __name__ == '__main__':

    while True:
        schedule.run_pending()
        time.sleep(1)
