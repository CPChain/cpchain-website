import time

import schedule
from pymongo import MongoClient



EVERYDAY = 1000
FAUCET_VALUE = 1
LIMIT_COIN = 10
DAY_SECENDS = 60 * 60 * 24

CLIENT = MongoClient(host='127.0.0.1', port=27017)
faucet_collection = CLIENT['cpchain']['faucet']


def coin_update():
    faucet_collection.update({}, {"$set": {"coins_daily": EVERYDAY}}, True)

schedule.every().day.do(coin_update)



if __name__ == '__main__':

    while True:
        schedule.run_pending()
        time.sleep(1)
