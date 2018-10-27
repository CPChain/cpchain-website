from django.shortcuts import render, redirect
from django.http import HttpResponse

from dwebsocket import accept_websocket
import time
import json
from pymongo import MongoClient, DESCENDING
from pure_pagination import Paginator, PageNotAnInteger
from cpchain_test.settings import web3
import hexbytes

ADD_SIZE = 42
CLIENT = MongoClient(host='127.0.0.1', port=27017)


def explorer(request):
    return render(request, 'explorer.html')


@accept_websocket
def wshandler(req):
    # index websocket handler
    msg = req.websocket.wait(1)
    msg = json.loads(msg)
    task = msg['event']
    block_collection = CLIENT['test']['blocks']
    txs_collection = CLIENT['test']['txs']
    if task == 'gs':
        while 1:
            height = block_collection.find().sort('_id', DESCENDING).limit(1)[0]['number']
            txs_count = txs_collection.find().count()

            # 测试用，传5个块
            b_li = list(block_collection.find({'number': {'$lte': height}}).sort('number', DESCENDING).limit(5))
            t_li = list(txs_collection.find().sort('date', DESCENDING).limit(5))

            index_info = {
                'height': height,
                'txs_count': txs_count
            }
            temp_num = min(height, txs_count, 5)

            for i in range(temp_num):
                index_info['b' + str(i)] = {
                    'number': b_li[i]['number'],
                    'miner': b_li[i]['miner'],
                    'txs': len(b_li[i]['transactions']),
                    'time': b_li[i]['timestamp']
                }
                index_info['t' + str(i)] = {
                    'txhash': t_li[i]['hash'],
                    'from': t_li[i]['from'],
                    'to': t_li[i]['to'],
                    'time': t_li[i]['date']
                }

            data = json.dumps(index_info)
            req.websocket.send(data)
            time.sleep(0.3)


def search(req):
    # address/contract  42/40
    # number  <42
    # block hash 66/64
    # tx hash 66/64

    search = req.GET.get('q').strip().lower()
    if len(search) < ADD_SIZE - 2:
        if not search.isdigit():
            return HttpResponse('string error!')
        return redirect('/block/' + search)
    elif len(search) <= ADD_SIZE:
        if web3.eth.getCode(search) == hexbytes.HexBytes('0x'):
            return redirect('/address/' + search)
        else:
            return redirect('/contract/' + search)
    else:
        # get Transaction info
        if not search.startswith('0x'):
            search = '0x' + search
        result = web3.eth.getTransaction(search)
        if result:
            return redirect('/tx/' + search)
        else:
            # get Block info
            return redirect('/block/' + search)


def blocks(req):
    # blocks
    collections = CLIENT['test']['blocks']
    all_blocks = list(collections.find().sort('number', DESCENDING))

    try:
        page = req.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(all_blocks, 25, request=req)
    blocks = p.page(page)
    return render(req, 'block_list.html', {'blocks': blocks})


def block(req, block_identifier):
    # search block by block_identifier
    search = block_identifier.strip().lower()
    collection = CLIENT['test']['blocks']
    if len(search) < ADD_SIZE - 2:
        # search by number
        block_dict = collection.find({'number': int(search)})[0]
    elif len(search) <= ADD_SIZE:
        # search by addr
        block_dict = collection.find({"address": search})[0]
    else:
        block_dict = collection.find({"hash": search})[0]

    height = block_dict['number']
    block_hash = block_dict['hash']
    parentHash = block_dict['parentHash']
    timestamp = block_dict['timestamp']
    txs = len(block_dict['transactions'])
    miner = block_dict['miner']
    size = block_dict['size']
    gasUsed = block_dict['gasUsed']
    gasLimit = block_dict['gasLimit']
    # blockReward = block_dict['']
    extraData = block_dict['extraData']

    return render(req, 'block_info.html', locals())


def txs(req):
    # txs
    collections = CLIENT['test']['txs']
    block = req.GET.get('block')
    if block == None:
        try:
            page = req.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        all_txs = collections.find().sort('_id', DESCENDING)
        p = Paginator(all_txs, 25, request=req)
        txs = p.page(page)
        return render(req, 'txs_list.html', {'txs': txs})
    # block's type is string
    txs_from_block = list(collections.find({'blockNumber': int(block)}))
    # page
    try:
        page = req.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    all_txs = txs_from_block
    p = Paginator(all_txs, 25, request=req)
    txs = p.page(page)
    return render(req, 'txs_from_block.html', {'txs': txs, 'blockNumber': block})


def tx(req, tx_hash):
    # tx from hash

    search = tx_hash.strip().lower()
    collection = CLIENT['test']['txs']
    tx_dict = list(collection.find({"hash": search}))[0]
    status = web3.eth.getTransactionReceipt(search).status
    if status == 1:
        tx_dict['status'] = 'Success'
    elif status == 0:
        tx_dict['status'] = 'Pending'
    else:
        tx_dict['status'] = status
    return render(req, 'tx_info.html', {'tx_dict': tx_dict})


def address(req, address):
    # address info
    address = web3.toChecksumAddress(address).strip().lower()
    collection = CLIENT['test']['txs']
    txs = list(collection.find({'$or': [{'from': address}, {'to': address}]}))

    # set in/out
    for d in txs:
        if d['from'] == d['to']:
            d['flag'] = 'self'
        elif d['from'] == address:
            d['flag'] = 'out'
        else:
            d['flag'] = 'in'

    txs.sort(key=lambda x: x['date'], reverse=True)
    raw_address = web3.toChecksumAddress(address)
    balance = web3.eth.getBalance(raw_address)
    txs_count = len(txs)

    # latest 25 txs
    if txs_count > 25:
        txs = txs[:25]

    return render(req, 'address.html', {'txs': txs,
                                        'address': raw_address,
                                        'balance': balance,
                                        'txs_count': txs_count
                                        })


def contract(req, contract):
    return render(req, 'contract.html')
