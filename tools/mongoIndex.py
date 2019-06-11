from pymongo import MongoClient
from cpchain_test.config import cfg

mongoHost = cfg['db']['ip']
port = int(cfg['db']['port'])

client = MongoClient(host=mongoHost, port=port)
b_collection = client['cpchain']['blocks']
tx_collection = client['cpchain']['txs']


def create_index():
    # block collection
    b_collection.create_index([('number', 1)])
    b_collection.create_index([('hash', 1)])
    b_collection.create_index([('miner', 1), ('timestamp', 1)])
    # txs collection
    tx_collection.create_index([('blockNumber', 1)])
    tx_collection.create_index([('hash', 1)])
    tx_collection.create_index([('from', 1)])
    tx_collection.create_index([('to', 1)])
    tx_collection.create_index([('timestamp', -1)])
    tx_collection.create_index([('from', 1), ('timestamp', -1)])
    tx_collection.create_index([('to', 1), ('timestamp', -1)])


if __name__ == '__main__':
    create_index()
