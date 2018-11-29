import logging
import logging.handlers
import time

import hexbytes
from pymongo import DESCENDING, MongoClient

from cpc_fusion import Web3
from cpc_fusion.middleware import geth_poa_middleware

logging.basicConfig(level=logging.INFO,
                    filename='./log/chain.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
logger = logging.getLogger(__name__)
rf_handler = logging.handlers.TimedRotatingFileHandler(filename="./log/chain.log", when='midnight', backupCount=10)
logger.addHandler(rf_handler)

cf = Web3(Web3.HTTPProvider('http://54.87.26.24:8503'))

cf.middleware_stack.inject(geth_poa_middleware, layer=0)
client = MongoClient(host='127.0.0.1', port=27017)
# blocks
b_collection = client['test']['blocks']
# txs
tx_collection = client['test']['txs']


def save_blocks_txs(start_block_id=None):
    # save blocks and it's txs to mongo
    temp_id = start_block_id
    logger.info('start block :#%d', temp_id)
    # chain restart
    if cf.cpc.blockNumber + 1 < start_block_id:
        b_collection.drop()
        tx_collection.drop()
        temp_id = 0

    while True:
        b_number = cf.cpc.blockNumber
        if b_number >= temp_id:
            # save one block
            block = dict(cf.cpc.getBlock(temp_id))
            block_ = block_formatter(block)
            b_collection.save(block_)
            logger.info('saving block: #%s', str(temp_id))
            # save txs in this block
            logger.info('scaning txs from block: #%s', str(temp_id))
            timestamp = block['timestamp']
            transaction_cnt = cf.cpc.getBlockTransactionCount(temp_id)
            txs_li = []
            for transaction_id in range(0, transaction_cnt):
                tx = dict(cf.cpc.getTransactionByBlock(temp_id, transaction_id))
                tx_ = tx_formatter(tx, timestamp)
                txs_li.append(tx_)
                # append 1 block's txs into txs_li
            if txs_li:
                tx_collection.insert_many(txs_li)
                logger.info('saving tx: block = %d, txs_count = %d', temp_id, transaction_cnt)
            temp_id += 1
        else:
            time.sleep(0.2)


def block_formatter(block):
    block_ = {}
    # hex_to_int = ['difficulty', 'gasLimit', 'gasUsed', 'number', 'size', 'timestamp', 'totalDifficulty']
    for k, v in block.items():
        if k == 'miner':
            block_[k] = v.lower()
        elif type(v) == hexbytes.HexBytes:
            block_[k] = v.hex()
        else:
            block_[k] = v
    return block_


def tx_formatter(tx, timestamp):
    tx_ = {}
    # hex_to_int = ['blockNumber', 'gas', 'gasPrice', 'transactionIndex']
    for k, v in tx.items():
        if type(v) == hexbytes.HexBytes:
            tx_[k] = v.hex()
        elif k == 'from' or k == 'to':
            if v:
                tx_[k] = v.lower()
            else:
                tx_[k] = v
        else:
            tx_[k] = v
    tx_['timestamp'] = timestamp
    tx_['txfee'] = tx_['gas'] / tx_['gasPrice']
    return tx_


def main():
    while True:
        # get the latest block id from db
        try:
            start_block_id = b_collection.find().sort('number', DESCENDING).limit(1)[0]['number'] + 1
        except IndexError:
            start_block_id = 0
            logger.warning('start from 0')

        try:
            save_blocks_txs(start_block_id)
        except Exception as e:
            logger.exception('main loop')
        time.sleep(10)


if __name__ == '__main__':
    main()
