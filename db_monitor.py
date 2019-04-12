import logging
import logging.handlers
import time

import hexbytes
from cpc_fusion import Web3
from cpc_fusion.middleware import geth_poa_middleware
from decorator import contextmanager
from pymongo import DESCENDING, MongoClient

from cpchain_test.config import cfg

REFRESH_INTERVAL = 3

# log
logging.basicConfig(level=logging.INFO,
                    filename='./log/chain.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
logger = logging.getLogger(__name__)
rf_handler = logging.handlers.TimedRotatingFileHandler(filename="./log/chain.log", when='midnight', backupCount=10)
logger.addHandler(rf_handler)

# chain

chain = 'http://{0}:{1}'.format(cfg['chain']['ip'], cfg['chain']['port'])
cf = Web3(Web3.HTTPProvider(chain))
cf.middleware_stack.inject(geth_poa_middleware, layer=0)

# mongodb
mongoHost = cfg['db']['ip']
client = MongoClient(host=mongoHost, port=27017)
b_collection = client['cpchain']['blocks']
tx_collection = client['cpchain']['txs']
address_collection = client['cpchain']['address']
contract_collection = client['cpchain']['contract']
event_collection = client['cpchain']['event']


def save_blocks_txs(start_block_id):
    '''
    save blocks and it's txs to mongo
    :param start_block_id:  start_block_id
    :return:
    '''
    temp_id = start_block_id
    logger.info('start block id : #%d', temp_id)

    # chain judge the newest block

    while True:
        b_number = cf.cpc.blockNumber
        if b_number >= temp_id:
            # save one block
            block = dict(cf.cpc.getBlock(temp_id))
            block_ = block_formatter(block)
            # save txs in this block
            logger.info('scaning txs from block: #%s', str(temp_id))
            timestamp = block_['timestamp']
            transaction_cnt = cf.cpc.getBlockTransactionCount(temp_id)
            txs_li = []

            all_txs = cf.cpc.getAllTransactionsByBlock(temp_id)
            for tx in all_txs:
                # save one tx
                status = tx.get('status')
                _tx = tx_formatter(tx, timestamp, status)
                txs_li.append(_tx)

                # scan contract
                if tx['isContract']:
                    contract = _tx.get('contractAddress')
                    creator = _tx.get('creator')
                    code = _tx.get('code')
                    contract_dict = {'txhash': _tx['hash'],
                                     'address': contract,
                                     'creator': creator,
                                     'blockNumber': temp_id,
                                     'code': code,
                                     }
                    contract_collection.insert_one(contract_dict)

                # address growth
                for add in [_tx['from'], _tx['to']]:
                    if add and address_collection.find({'address': add}).count() == 0:
                        address_collection.insert_one({'address': add, 'timestamp': timestamp})
                # jianhua's code
                # if len(_tx['input']) >= 10:
                #     method = _tx['input'][:10]
                # else:
                #     method = _tx['input']
                #
                # for log in tx_receipt.logs:
                #     topics = []
                #     for topic in log.topics:
                #         topics.append(topic.hex())
                #
                #     event_collection.insert_one(
                #         {
                #             'contract_address': log.address,
                #             'txhash': log.transactionHash.hex(),
                #             'block': log.blockNumber,
                #             'timestamp': timestamp,  # block timestamp
                #             'method': method,
                #             'topics': topics,
                #             'data': log.data,
                #         }
                #     )

            # append 1 block's txs into txs_li
            if txs_li:
                tx_collection.insert_many(txs_li)
                logger.info('saving tx: block = %d, txs_count = %d', temp_id, transaction_cnt)
            reward = update_reward(temp_id)
            block_['reward'] = reward
            b_collection.save(block_)
            logger.info('saving block: #%s', str(temp_id))

            temp_id += 1
        else:
            time.sleep(REFRESH_INTERVAL)


def update_reward(id):
    reward = get_block_reward(id)
    logger.info('reward')
    logger.info(reward)
    return reward


def block_formatter(block):
    block_ = {}
    # hex_to_int = ['difficulty', 'gasLimit', 'gasUsed', 'number', 'size', 'timestamp']
    for k, v in block.items():
        if k == 'miner':
            block_[k] = v.lower()
            if block_[k].endswith('00000000'):
                try:
                    block_['impeachProposer'] = cf.cpc.getProposerByBlock(block['number'])
                except Exception as e:
                    logger.info('getProposerByBlock error:', e)
                    block_['impeachProposer'] = '0x'
        elif k == 'timestamp':
            block_[k] = v / 1000
        elif type(v) == hexbytes.HexBytes:
            block_[k] = v.hex()
        else:
            block_[k] = v
    return block_


@contextmanager
def timer(name):
    start = time.time()
    yield
    logger.info(f'[{name}] done in {time.time() - start:.2f} s')


def get_block_value(p, number):
    if number == 0:
        return 0
    p = p.lower()
    logger.info('proposer:%s' % p)
    logger.info('number:%s' % number)
    in_txs = list(tx_collection.find({'blockNumber': number, 'to': p}))
    in_v = 0
    out_v = 0
    for tx in in_txs:
        in_v += tx['value']
    # logger.info('in_value')
    # logger.info(in_v)
    out_txs = list(tx_collection.find({'blockNumber': number, 'from': p}))
    for tx in out_txs:
        out_v += tx['value']
    # logger.info('out_value')
    # logger.info(out_v)
    return in_v - out_v


def get_block_reward(number):
    if number == 0:
        return 0
    try:
        p = cf.cpc.getProposerByBlock(number)
    except Exception as e:
        logger.info('getProposerByBlock error:', e)
        return 0
    p = cf.toChecksumAddress(p)
    current_balance = cf.cpc.getBalance(p, number)
    last_balance = cf.cpc.getBalance(p, number - 1)
    value_in_block = get_block_value(p, number)
    reward = current_balance - last_balance - value_in_block
    return str(cf.fromWei(reward, 'ether'))


def tx_formatter(tx, timestamp, status):
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
        if k == 'value':
            tx_[k] = float(v)
    # TODO need gasused from receipt
    tx_['gasUsed'] = tx['gasUsed']
    tx_['timestamp'] = timestamp
    tx_['status'] = status
    tx_['txfee'] = tx_['gasUsed'] * tx_['gasPrice'] / 10 ** 18
    return tx_


def start_block(start_block_id_from_db):
    block_id_from_chain = cf.cpc.blockNumber

    if block_id_from_chain >= start_block_id_from_db:
        # check db_block's hash
        if check_block_hash(start_block_id_from_db):
            return start_block_id_from_db
        else:
            return 0
    else:
        logger.warning('block_id_from_chain is less than db !!! empty db...')
        return 0


#
# def find_block(block_id):
#     start_id = block_id
#     while not check_block_hash(start_id) and start_id > 0:
#         start_id -= 1
#     logger.warning('find the latest valid block:%d', start_id)
#     return start_id


def get_block_from_db(b_id):
    return b_collection.find({'number': b_id})[0]


def check_block_hash(block_id):
    block_hash_db = get_block_from_db(block_id)['hash']
    block_hash_chain = cf.toHex(cf.cpc.getBlock(block_id).hash)
    return True if block_hash_chain == block_hash_db else False


def remove_data_from_db():
    logger.warning('start remove data from block:%d')
    b_collection.delete_many({'number': {'$gte': 0}})
    tx_collection.delete_many({'blockNumber': {'$gte': 0}})
    contract_collection.delete_many({'blockNumber': {'$gte': 0}})


def main():
    while True:
        # get the latest block id from db
        try:
            last_block_id_from_db = b_collection.find().sort('number', DESCENDING).limit(1)[0]['number']
        except IndexError:
            last_block_id_from_db = 0
            logger.warning('initial cpchain  ... !!!')

        if last_block_id_from_db:
            try:
                last_valid_block_id = start_block(last_block_id_from_db)
            except Exception as e:
                logger.info(e)
                time.sleep(10)
                continue
        else:
            last_valid_block_id = 0
        start_block_id = last_valid_block_id + 1 if last_valid_block_id else 0
        logger.info('start block id =%d', start_block_id)
        # remove invalid data from db
        if start_block_id == 0:
            remove_data_from_db()

        try:
            save_blocks_txs(start_block_id)
        except Exception as e:
            logger.exception('save_blocks_txs error: ', e)
        time.sleep(10)


if __name__ == '__main__':
    print('start')
    main()
