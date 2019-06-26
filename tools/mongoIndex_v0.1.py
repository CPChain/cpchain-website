from pymongo import MongoClient

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


def update_index():
    # block collection
    b_collection.drop_index([('miner', 1), ('timestamp', 1)])
    b_collection.create_index([('miner', 1), ('_id', -1)])

    # txs collection


if __name__ == '__main__':
    update_index()
