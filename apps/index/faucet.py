import threading
import time

from cpc_fusion import Web3
from pymongo import MongoClient

from cpchain_test.config import cfg

faucet_chain = 'http://{0}:{1}'.format(cfg['faucet']['ip'], cfg['faucet']['port'])
cf = Web3(Web3.HTTPProvider(faucet_chain))

FAUCET_VALUE = int(100 * 1e+18)
LIMIT_COIN = int(100 * 1e+18)
DAY_SECENDS = 60 * 60 * 24

mongo = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])

CLIENT = MongoClient(host=mongo, port=port)
faucet_collection = CLIENT['cpchain']['faucet']
SEND_ACCOUNT = cfg['faucet']['account']
PWD = cfg['faucet']['password']


class Faucet:

    @staticmethod
    def send(addr):
        def _send(addr):
            account = cf.toChecksumAddress(addr)
            print(cf.personal.sendTransaction({'to': account, 'from': SEND_ACCOUNT, 'value': FAUCET_VALUE},
                                              PWD))

        threading.Thread(target=_send, args=(addr,)).start()

    @staticmethod
    def valid():
        # coins everyday
        coins = faucet_collection.find({})[0]['coins_daily']
        return True if coins > 0 else False

    @staticmethod
    def update(addr):
        coins = faucet_collection.find({})[0]['coins_daily']
        faucet_collection.update({'coins_daily': {'$exists': True}}, {"$set": {"coins_daily": coins - FAUCET_VALUE}})
        faucet_collection.insert_one(
            {'address': addr, 'value': float(FAUCET_VALUE), 'time': time.time()})

    @staticmethod
    def limit(address):
        now = int(time.time())
        day_zero = now - now % DAY_SECENDS
        addrs = faucet_collection.find({'address': address, 'time': {'$gte': day_zero, '$lt': now}})
        addr_coins = 0
        for _ in addrs:
            addr_coins += _['value']
        return True if addr_coins < LIMIT_COIN else False
