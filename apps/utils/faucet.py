import time
import sys, os

import schedule
from pymongo import MongoClient

sys.path.insert(0, os.getcwd())
from cpchain_test.config import cfg

EVERYDAY = 1000000 * 1e+18

mongo = cfg['db']['ip']
CLIENT = MongoClient(host=mongo, port=27017)
faucet_collection = CLIENT['cpchain']['faucet']


def coin_update():
    faucet_collection.update({'coins_daily': {'$exists': True}}, {"$set": {"coins_daily": EVERYDAY}}, True)


schedule.every().day.do(coin_update)


if __name__ == '__main__':

    while True:
        schedule.run_pending()
        time.sleep(1)
