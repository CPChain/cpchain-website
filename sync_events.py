"""

事件同步

sudo docker run -it --name sync_events -v `pwd`:/cpchain-website liaojl/website python sync-events.py

"""


import logging
import logging.handlers
import time
import json

import hexbytes
from cpc_fusion import Web3
from decorator import contextmanager
from pymongo import DESCENDING, MongoClient

from cpchain_test.config import cfg
from tools.dingding import post_message

DAY_SECENDS = 60 * 60 * 24
REFRESH_INTERVAL = 10

logger_format = '[%(levelname)s][%(asctime)s][%(name)s:%(lineno)d]%(message)s'

# log
logging.basicConfig(level=logging.INFO,
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format=logger_format)

logger = logging.getLogger('sync-event')

rf_handler = logging.handlers.TimedRotatingFileHandler(
    filename="./logs/sync-events.log", when='midnight', backupCount=10)
formatter = logging.Formatter(logger_format)
rf_handler.setFormatter(formatter)

logger.addHandler(rf_handler)

# chain config
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

events_col = db['dapps_events']
events_meta = db['dapps_events_meta']

contract_abi = "[{\"constant\":true,\"inputs\":[],\"name\":\"count\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"enabled\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"enableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"receivedCount\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"disableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"sentCount\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"to\",\"type\":\"address\"},{\"name\":\"message\",\"type\":\"string\"}],\"name\":\"sendMessage\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"inputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"from\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"to\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"sentID\",\"type\":\"uint256\"},{\"indexed\":false,\"name\":\"recvID\",\"type\":\"uint256\"},{\"indexed\":false,\"name\":\"message\",\"type\":\"string\"}],\"name\":\"NewMessage\",\"type\":\"event\"}]"
contract_address = "0x856c36486163dB6f9aEbeD1407a3c6C51FD7566E"

identity_abi = "[{\"constant\":true,\"inputs\":[],\"name\":\"count\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"enabled\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"enableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"disableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"remove\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"get\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"content\",\"type\":\"string\"}],\"name\":\"register\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"inputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"identity\",\"type\":\"string\"}],\"name\":\"NewIdentity\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"identity\",\"type\":\"string\"}],\"name\":\"UpdateIdentity\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"}],\"name\":\"RemoveIdentity\",\"type\":\"event\"}]"
identity_addr = "0xC53367856164DA3De57784E0c96710088DA77e20"


@contextmanager
def timer(name):
    start = time.time()
    yield
    logger.info(f'[{name}] done in {time.time() - start:.2f} s')


def get_event_names(abi):
    abi_parsed = json.loads(abi)
    event_names = []
    for item in abi_parsed:
        if item.get('type') == 'event':
            event_names.append(item['name'])
    return event_names


def sync_events(start_at):
    '''
    save blocks and it's txs to mongo
    :param start_block_id:  start_block_id
    :return:
    '''
    temp_id = start_at
    while True:
        b_number = cf.cpc.blockNumber
        if b_number >= temp_id:
            logger.info("sync block %d", temp_id)
            # iterate all abis and their own events
            contracts = [
                (contract_abi, contract_address),
                (identity_abi, identity_addr),
            ]
            for contract in contracts:
                event_names = get_event_names(contract[0])
                instance = cf.cpc.contract(
                    abi=contract[0], address=contract[1])
                for event_name in event_names:
                    events = instance.events[event_name]().createFilter(
                        fromBlock=temp_id).get_all_entries()
                    for e in events:
                        e = event_formatter(e)
                        if events_col.count_documents({"event": e['event'], "transactionHash": e['transactionHash']}) == 0:
                            logger.info("insert event:%s and tx:%s",
                                        e['event'], e['transactionHash'])
                            block = cf.cpc.getBlock(e['blockNumber'])
                            e['timestamp'] = block['timestamp']
                            events_col.insert_one(e)
            update_current(events_meta, temp_id)
            temp_id += 1
        else:
            time.sleep(REFRESH_INTERVAL)


def event_formatter(e):
    _e = {}
    for k, v in e.items():
        if isinstance(v, type(e)):
            v = event_formatter(v)
        elif type(v) == hexbytes.HexBytes:
            v = v.hex()
        _e[k] = v
    return _e


def get_current(col):
    return col.find()[0]['current_block']


def update_current(col, current):
    col.update_one({'current_block': {'$exists': True}},  {
                   "$set": {'current_block': current}}, True)


def main():
    while True:
        try:
            logger.info('Sync started')
            # get the latest block id from meta collection
            if events_meta.count_documents({}) == 0:
                # insert the first meta info
                events_meta.insert_one({
                    'current_block': 4884651,
                })
            lastest_num = get_current(events_meta)
            lastest_num = 4884651

            logger.info("latest block %d", lastest_num)

            if lastest_num == 0:
                start_at = 0
            else:
                start_at = lastest_num + 1

            logger.info('start block: %d', start_at)
            sync_events(start_at)
        except Exception as e:
            logger.error(f'loop error: {e}')
            try:
                post_message(f"**sync-events error:**\n{e}")
            except Exception as e:
                logger.error(f'post message error_db sync error:{e}')
        time.sleep(10)


if __name__ == '__main__':
    main()
