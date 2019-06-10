import time
import sys, os

import schedule
from pymongo import MongoClient

sys.path.insert(0, os.getcwd())
from cpchain_test.config import cfg

EVERYDAY = 100000 * 1e+18

mongo = cfg['db']['ip']
port = int(cfg['db']['port'])

CLIENT = MongoClient(host=mongo, port=port)
faucet_collection = CLIENT['cpchain']['faucet']


def coin_update():
    faucet_collection.update({'coins_daily': {'$exists': True}}, {"$set": {"coins_daily": EVERYDAY}}, True)


schedule.every().day.do(coin_update)


if __name__ == '__main__':

    while True:
        schedule.run_pending()
        time.sleep(1)
