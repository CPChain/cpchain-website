import time

from cpc_fusion import Web3
from pymongo import MongoClient

from cpchain_test.config import cfg

REFRESH_INTERVAL = 3

# chain

chain = 'http://{0}:{1}'.format(cfg['chain']['ip'], cfg['chain']['port'])
cf = Web3(Web3.HTTPProvider(chain))

# mongodb
mongoHost = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])

client = MongoClient(host=mongoHost, port=port)
uname = cfg['mongo']['uname']
pwd = cfg['mongo']['password']
db = client['cpchain']
db.authenticate(uname, pwd)
rnode_collection = client['cpchain']['rnode']
proposer_collection = client['cpchain']['proposer']
block_collection = client['cpchain']['blocks']
txs_collection = client['cpchain']['txs']
num_collection = client['cpchain']['num']


def update_rate():
    spend_time = 60 * 10
    start_timestamp = int(time.time()) - spend_time
    txs_count = txs_collection.find({'timestamp': {'$gte': start_timestamp}}).count()
    print('tps updating...')
    num_collection.update({'type': 'tps'}, {'$set': {'tps': round(txs_count / spend_time, 2)}}, upsert=True)
    # update bps
    block_count = block_collection.find({'timestamp': {'$gte': start_timestamp}}).count()
    print('bps updating...')
    num_collection.update({'type': 'bps'}, {'$set': {'bps': round(block_count / spend_time, 2)}}, upsert=True)


def main():
    while True:
        try:
            update_rate()
        except Exception as e:
            print('rate update Error >>>', e)
        time.sleep(10)


if __name__ == '__main__':
    print('rate update start')
    main()
