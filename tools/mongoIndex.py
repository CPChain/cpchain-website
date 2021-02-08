from pymongo import MongoClient

import sys
sys.path.append('..')

from cpchain_test.config import cfg

mongoHost = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])

client = MongoClient(host=mongoHost, port=port)
uname = cfg['mongo']['uname']
pwd = cfg['mongo']['password']
db = client['cpchain']
db.authenticate(uname, pwd)
b_collection = client['cpchain']['blocks']
tx_collection = client['cpchain']['txs']


def create_index():
    # block collection
    b_collection.create_index([('number', 1)])
    b_collection.create_index([('hash', 1)])
    b_collection.create_index([('timestamp', 1)])
    b_collection.create_index([('miner', 1), ('timestamp', 1)])
    
    # txs collection
    tx_collection.create_index([('blockNumber', 1)])
    tx_collection.create_index([('hash', 1)])
    tx_collection.create_index([('from', 1)])
    tx_collection.create_index([('to', 1)])
    tx_collection.create_index([('timestamp', -1)])
    tx_collection.create_index([('from', 1), ('timestamp', -1)])
    tx_collection.create_index([('to', 1), ('timestamp', -1)])

    # 2021/01/29 增加 value 的索引
    tx_collection.create_index([('value', 1)])
    tx_collection.create_index([('from', 1), ('value', 1)])
    tx_collection.create_index([('to', 1), ('value', 1)])
    tx_collection.create_index([('from', 1), ('to', 1), ('value', 1)])


if __name__ == '__main__':
    create_index()
