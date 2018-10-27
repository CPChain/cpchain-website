from pymongo import MongoClient, DESCENDING
import time
from datetime import datetime
import hexbytes
from multiprocessing import Process

from cpchain_test.settings import web3


def save_blocks(start_block_id=None):
    client = MongoClient(host='127.0.0.1', port=27017)
    # save blocks to mongo
    start_block_id = start_block_id or 0
    collection = client['test']['blocks']
    temp_id = start_block_id
    print('start block :#{}'.format(temp_id))
    try:
        if web3.eth.blockNumber + 1 < start_block_id:
            collection.drop()
            temp_id = 0
    except Exception:
        pass
    while 1:
        try:
            b_number = web3.eth.blockNumber
            if b_number >= temp_id:
                block = dict(web3.eth.getBlock(temp_id))
                block_ = block_formatter(block)
                collection.save(block_)
                print('saving block: #' + str(temp_id) + time.asctime()[:-5])
                temp_id += 1
            else:
                time.sleep(0.2)
        except Exception as e:
            print('block E:', e)
            break


def save_transaction(start_tx_block_id=None):
    # scan all blocks by default
    client = MongoClient(host='127.0.0.1', port=27017)
    start_tx_block_id = start_tx_block_id or 0
    collection = client['test']['txs']
    block_id = start_tx_block_id
    print('start scaning txs from block: #{}'.format(start_tx_block_id))

    try:
        if web3.eth.blockNumber + 1 < start_tx_block_id:
            collection.drop()
            block_id = 0
    except Exception:
        pass

    while 1:
        try:
            b_height = web3.eth.blockNumber
            if b_height >= block_id:
                print('scaning txs from block: #', block_id, time.asctime()[:-5])
                timestamp = web3.eth.getBlock(block_id).timestamp
                timestamp = datetime.fromtimestamp(timestamp).isoformat()
                transaction_cnt = web3.eth.getBlockTransactionCount(block_id)
                txs_li = []
                for transaction_id in range(0, transaction_cnt):
                    tx = dict(web3.eth.getTransactionByBlock(block_id, transaction_id))
                    tx_ = tx_formatter(tx, timestamp)
                    txs_li.append(tx_)
                    # append 1 block's txs into txs_li
                if txs_li:
                    collection.insert_many(txs_li)
                    print('saving tx: block = {0} , txs_count = {1}, --{2}'.format(block_id, transaction_cnt,
                                                                                   time.asctime()[:-5]))
                block_id += 1
            else:
                time.sleep(0.2)
        except Exception as e:
            print('txs E:', e)
            break


def block_formatter(block):
    block_ = {}
    for k, v in block.items():
        if type(v) == hexbytes.main.HexBytes:
            block_[k] = v.hex()
        elif k == 'miner':
            block_[k] = v.lower()
        elif k == 'timestamp':
            block_[k] = datetime.fromtimestamp(v).isoformat()
        else:
            block_[k] = v
    return block_


def tx_formatter(tx, timestamp):
    tx_ = {}
    for k, v in tx.items():
        if type(v) == hexbytes.main.HexBytes:
            tx_[k] = v.hex()
        elif k == 'from' or k == 'to':
            if v:
                tx_[k] = v.lower()
            else:
                tx_[k] = v
        else:
            tx_[k] = v
    tx_['date'] = timestamp
    tx_['value'] = str(tx['value'])
    tx_['txfee'] = tx['gas'] / tx['gasPrice']
    return tx_


def main():
    client = MongoClient(host='127.0.0.1', port=27017)

    # blocks
    b_collection = client['test']['blocks']
    try:
        start_block_id = b_collection.find().sort('number', DESCENDING).limit(1)[0]['number'] + 1
    except IndexError:
        start_block_id = 0
    p1 = Process(target=save_blocks, args=(start_block_id,))

    # txs
    t_collection = client['test']['txs']
    try:
        start_tx_block_id = t_collection.find().sort('_id', DESCENDING).limit(1)[0]['blockNumber'] + 1
    except IndexError:
        start_tx_block_id = 0
    p2 = Process(target=save_transaction, args=(start_tx_block_id,))

    # start process
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    time.sleep(10)
    main()


if __name__ == '__main__':
    main()
