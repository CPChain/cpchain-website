"""

db.py

"""

from cpchain_test.config import cfg
from log import get_log

from pymongo import DESCENDING, MongoClient

RNODE_REWARD_META = 'rnode_reward_meta'
RNODE_REWARD_TOTEL = 'rnode_reward_total'
RNODE_REWARD_HISTORY = 'rnode_reward_history'

log = get_log('app')

mongo = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])

CLIENT = MongoClient(host=mongo, port=port, maxPoolSize=200)
uname = cfg['mongo']['uname']
pwd = cfg['mongo']['password']
db = CLIENT['cpchain']
db.authenticate(uname, pwd)

cpchain_db = CLIENT['cpchain']

block_collection = CLIENT['cpchain']['blocks']
txs_collection = CLIENT['cpchain']['txs']

rnode_col = CLIENT['rnode']

rnode_reward_meta_col = db[RNODE_REWARD_META]
rnode_reward_total_col = db[RNODE_REWARD_TOTEL]
rnode_reward_history = db[RNODE_REWARD_HISTORY]
