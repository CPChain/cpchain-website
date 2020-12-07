"""

db.py

"""

from cpchain_test.config import cfg
from log import get_log

from pymongo import DESCENDING, MongoClient

log = get_log('app')

mongo = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])

CLIENT = MongoClient(host=mongo, port=port, maxPoolSize=200)
uname = cfg['mongo']['uname']
pwd = cfg['mongo']['password']
db = CLIENT['cpchain']
db.authenticate(uname, pwd)

block_collection = CLIENT['cpchain']['blocks']
txs_collection = CLIENT['cpchain']['txs']
