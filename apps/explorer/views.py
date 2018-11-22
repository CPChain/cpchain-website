import json
import time
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import redirect, render
from pure_pagination import PageNotAnInteger, Paginator
from pymongo import DESCENDING, MongoClient

try:
    import uwsgi
except:
    pass
from cpchain_test.settings import cpc_fusion as cf

ADD_SIZE = 42
CLIENT = MongoClient(host='127.0.0.1', port=27017)
block_collection = CLIENT['test']['blocks']
txs_collection = CLIENT['test']['txs']
DAY_SECENDS = 60 * 60 * 24


def explorer(request):
    rnode = len(cf.cpc.getRNodes())
    committee = len(cf.cpc.getCommittees())
    height = block_collection.find().sort('_id', DESCENDING).limit(1)[0]['number']
    b_li = list(block_collection.find({'number': {'$lte': height}}).sort('number', DESCENDING).limit(10))
    txs_count = txs_collection.find().count()
    b_li.reverse()
    b_li = b_li[:9]
    t_li = list(txs_collection.find().sort('timestamp', DESCENDING).limit(10))

    ## header
    # tps
    start_timestamp = block_collection.find({'number': 1})[0]['timestamp']
    current_timestamp = int(time.time())
    spend_time = current_timestamp - start_timestamp
    tps = txs_count / spend_time
    header = {
        'blockHeight': height,
        'txs': txs_count,
        'rnode': rnode,
        'tps': tps,
        'committee': committee,
    }

    ## chart
    # chart = [{
    #     'time': '11/22',
    #     'bk': 123,
    #     'tx': 321
    # }]
    now = int(time.time())
    day_zero = now - now % DAY_SECENDS
    chart = []
    for i in range(12):
        gt_time = day_zero - (i + 1) * DAY_SECENDS
        lt_time = day_zero - i * DAY_SECENDS
        now_ts = now - i * DAY_SECENDS
        time_local = time.localtime(now_ts)
        dt = time.strftime('%m/%d', time_local)
        txs_day = txs_collection.find({'timestamp': {'$gte': gt_time, '$lt': lt_time}})
        chart.append({'time': dt, 'tx': txs_day, 'bk': 0})

    # blocks
    blocks = []
    for b in b_li:
        block = {
            'id': b['number'],
            'reward': 0,
            'txs': 0,
            'producerID': b['miner'],
            'timestamp': b['timestamp'],
            'hash': b['hash'],
        }
        blocks.append(block)

    # txs
    txs = []
    for t in t_li:
        tx = {
            'hash': t['hash'],
            'sellerID': t['from'],
            'buyerID': t['to'],
            'timestamp': t['timestamp'],
            'amount': t['txfee']
        }
        txs.append(tx)

    return render(request, 'explorer/explorer.html',
                  {'blocks': blocks, 'header': json.dumps(header), 'txs': json.dumps(txs), 'chart': chart})


def wshandler(req):
    # index websocket handler
    uwsgi.websocket_handshake()
    temp_height = block_collection.find().sort('_id', DESCENDING).limit(1)[0]['number']
    while True:
        block = block_collection.find().sort('_id', DESCENDING).limit(1)[0]
        block_height = block['number']
        if block_height >= temp_height:
            txs_count = txs_collection.find().count()
            rnode = len(cf.cpc.getRNodes())
            committee = len(cf.cpc.getCommittees())

            data = {}
            # tps
            start_timestamp = block_collection.find({'number': 1})[0]['timestamp']
            current_timestamp = int(time.time())
            spend_time = current_timestamp - start_timestamp
            tps = txs_count / spend_time

            header = {
                'blockHeight': block_height,
                'txs': txs_count,
                'rnode': rnode,
                'tps': tps,
                'committee': committee,
            }
            temp = block_collection.find({'number': temp_height})[0]
            b_txs_count = len(temp['transactions'])
            block = {
                'id': temp_height,
                'reward': 0,
                'txs': b_txs_count,
                'producerID': temp['miner'],
                'timestamp': temp['timestamp'],
                'hash': temp['hash'],
            }
            t_li = list(txs_collection.find().sort('timestamp', DESCENDING).limit(10))
            t_li.reverse()
            txs = []
            for t in t_li:
                tx = {
                    'hash': t['hash'],
                    'sellerID': t['from'],
                    'buyerID': t['to'],
                    'timestamp': t['timestamp'],
                    'amount': t['txfee']
                }
                txs.append(tx)
            data['header'] = header
            data['block'] = block
            data['txs'] = txs
            data = json.dumps(data)
            uwsgi.websocket_send(data)
            temp_height += 1
        else:
            time.sleep(0.3)


def search(req):
    """
    address/contract  42/40
    number  <42
    block hash 66/64
    tx hash 66/64
    """
    search = req.GET.get('q').strip().lower()
    if len(search) < ADD_SIZE - 2:
        # block number
        if not search.isdigit():
            return HttpResponse('string error!')
        return redirect('/explorer/block/' + search)
    elif len(search) <= ADD_SIZE:
        # address or contract
        return redirect('/explorer/address/' + search)
    else:
        # hash
        # get Transaction info
        if not search.startswith('0x'):
            search = '0x' + search
        result = txs_collection.find({'hash': search}).count()
        if result:
            return redirect('/explorer/tx/' + search)
        else:
            result = block_collection.find({'hash': search}).count()
            if result:
                # get Block info
                return redirect('/explorer/block/' + search)
            else:
                return HttpResponse('sorry,address not found')


def blocks(req):
    # blocks
    all_blocks = list(block_collection.find().sort('number', DESCENDING))

    try:
        page = req.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(all_blocks, 25, request=req)
    blocks = p.page(page)
    return render(req, 'explorer/block_list.html', {'blocks': blocks})


def block(req, block_identifier):
    # search block by block_identifier
    search = block_identifier.strip().lower()
    if len(search) < ADD_SIZE - 2:
        # search by number
        block_dict = block_collection.find({'number': int(search)})[0]
    elif len(search) <= ADD_SIZE:
        # search by addr
        block_dict = block_collection.find({"address": search})[0]
    else:
        block_dict = block_collection.find({"hash": search})[0]

    height = block_dict['number']
    block_hash = block_dict['hash']
    parentHash = block_dict['parentHash']
    timestamp = block_dict['timestamp']
    txs = len(block_dict['transactions'])
    miner = block_dict['miner']
    size = block_dict['size']
    gasUsed = block_dict['gasUsed']
    gasLimit = block_dict['gasLimit']
    # blockReward = block_dict['txfee']
    extraData = block_dict['proofOfAuthorityData']

    return render(req, 'explorer/block_info.html', locals())


def txs(req):
    # txs
    block = req.GET.get('block')
    if block == None:
        try:
            page = req.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        all_txs = txs_collection.find().sort('_id', DESCENDING)
        p = Paginator(all_txs, 25, request=req)
        txs = p.page(page)
        return render(req, 'explorer/txs_list.html', {'txs': txs})
    # block's type is string
    txs_from_block = list(txs_collection.find({'blockNumber': int(block)}))
    # page
    try:
        page = req.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    all_txs = txs_from_block
    p = Paginator(all_txs, 25, request=req)
    txs = p.page(page)
    return render(req, 'explorer/txs_from_block.html', {'txs': txs, 'blockNumber': block})


def tx(req, tx_hash):
    # tx from hash

    search = tx_hash.strip().lower()
    tx_dict = list(txs_collection.find({"hash": search}))[0]
    status = cf.eth.getTransactionReceipt(search).status
    if status == 1:
        tx_dict['status'] = 'Success'
    elif status == 0:
        tx_dict['status'] = 'Pending'
    else:
        tx_dict['status'] = status
    return render(req, 'explorer/tx_info.html', {'tx_dict': tx_dict})


def address(req, address):
    raw_address = cf.toChecksumAddress(address.strip())
    address = raw_address.lower()
    code = cf.eth.getCode(raw_address)
    code = cf.toHex(code)
    # address info
    txs = list(txs_collection.find({'$or': [{'from': address}, {'to': address}]}))
    # set in/out
    for d in txs:
        if d['from'] == d['to']:
            d['flag'] = 'self'
        elif d['from'] == address:
            d['flag'] = 'out'
        else:
            d['flag'] = 'in'

    txs.sort(key=lambda x: x['timestamp'], reverse=True)
    balance = cf.eth.getBalance(raw_address)
    txs_count = len(txs)

    # latest 25 txs
    if txs_count > 25:
        txs = txs[:25]

    if code == '0x':
        return render(req, 'explorer/address.html', {'txs': txs,
                                                     'address': raw_address,
                                                     'balance': balance,
                                                     'txs_count': txs_count
                                                     })
    else:
        return render(req, 'explorer/contract.html', {'txs': txs,
                                                      'address': raw_address,
                                                      'balance': balance,
                                                      'txs_count': txs_count,
                                                      'code': code,
                                                      })
