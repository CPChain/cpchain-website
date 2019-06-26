import os
import sys

from pymongo import MongoClient

sys.path.append('../..')
os.chdir(sys.path[0])
from cpchain_test.config import cfg

mongo = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])
CLIENT = MongoClient(host=mongo, port=port, maxPoolSize=200)

uname = cfg['mongo']['uname']
pwd = cfg['mongo']['password']
db = CLIENT['cpchain']
db.authenticate(uname, pwd)

txs_collection = db['txs']
address_collection = db['address']
address_txs_collection = db['address_txs']

block_number = 700644


def write_count():
    address_list = address_collection.find()
    total = address_list.count()
    i = 0
    for a in address_list:
        address = a.get('address').lower()
        txs = txs_collection.count(
            {'$and': [{'$or': [{'from': address}, {'to': address}]}, {'blockNumber': {'$lte': block_number}}]})
        print(f'{i}/{total}')
        print(f'addr: {address}, txs:{txs}')
        address_collection.update({'address': address}, {'$set': {'txs_count': txs}}, False, False)
        i += 1



if __name__ == '__main__':
    pass
    # write_count()
