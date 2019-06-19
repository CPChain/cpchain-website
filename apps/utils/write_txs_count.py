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

block_number = 685000


def write_count():
    address_list = address_collection.find()
    for a in address_list:
        address = a.get('address')
        print(address)
        count =



if __name__ == '__main__':
    write_count()
