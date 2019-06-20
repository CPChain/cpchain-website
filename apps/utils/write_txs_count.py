from pymongo import DESCENDING, MongoClient

import os, sys

sys.path.append('../..')
os.chdir(sys.path[0])

from cpchain_test.config import cfg

mongo = cfg['db']['ip']

port = int(cfg['db']['port'])
CLIENT = MongoClient(host=mongo, port=port, maxPoolSize=200)

uname = cfg['db']['uname']
pwd = cfg['db']['password']
db = CLIENT['cpchain']
db.authenticate(uname, pwd)

txs_collection = db['txs']
address_collection = db['address']
address_txs_collection = db['address_txs']

block_number = 685000


def write_count():
    address_list = address_collection.find()
    total = address_list.count()
    i = 0
    for a in address_list:
        t_list = []
        print(f'{i}/{total}')
        address = a.get('address').lower()
        print(address)
        txs = txs_collection.find({'$or': [{'from': address}, {'to': address}]}, {'_id': 0})
        t_count = txs.count()
        j = 0
        for t in txs:
            print('txs', j, t_count)
            t_list.append(t)
            j += 1
        addr_dict = {address: t_list}
        address_txs_collection.insert_one(addr_dict)
        i += 1


if __name__ == '__main__':
    write_count()
