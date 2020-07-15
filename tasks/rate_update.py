import time

from cpc_fusion import Web3
from pymongo import MongoClient

from log import get_log
from cpchain_test.config import cfg

REFRESH_INTERVAL = 3

log = get_log('rate-update')

# chain
chain = 'http://{0}:{1}'.format(cfg['chain']['ip'], cfg['chain']['port'])

# mongodb
mongoHost = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])


def update_rate():
    cf = Web3(Web3.HTTPProvider(chain))
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
    spend_time = 60 * 10
    start_timestamp = int(time.time()) - spend_time
    txs_count = txs_collection.find({'timestamp': {'$gte': start_timestamp}}).count()
    tps = round(txs_count / spend_time, 2)
    num_collection.update({'type': 'tps'}, {'$set': {'tps': tps}}, upsert=True)
    # update bps
    block_count = block_collection.find({'timestamp': {'$gte': start_timestamp}}).count()
    bps = round(block_count / spend_time, 2)
    num_collection.update({'type': 'bps'}, {'$set': {'bps': bps}}, upsert=True)
    client.close()
    log.info('tps: ' + str(tps) + ', bps: ' + str(bps))
