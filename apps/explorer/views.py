import json
import time
import threading

from django.shortcuts import redirect, render
from pure_pagination import PageNotAnInteger, Paginator
from pymongo import DESCENDING, MongoClient
from django.views.decorators.cache import cache_page

try:
    import uwsgi
except:
    print('uwsgi import error')

from cpchain_test.settings import cpc_fusion as cf

REFRESH_INTERVAL = 1
ADD_SIZE = 42
CLIENT = MongoClient(host='127.0.0.1', port=27017)
block_collection = CLIENT['cpchain']['blocks']
txs_collection = CLIENT['cpchain']['txs']
address_collection = CLIENT['cpchain']['address']

DAY_SECENDS = 60 * 60 * 24


class RNode:
    rnode = None
    rnode_length = 0
    updating = False

    @staticmethod
    def update():
        def _update():
            RNode.updating = True
            try:
                RNode.rnode = cf.cpc.getRNodes
            except Exception as e:
                print('rnode time out >>>>',e)
            RNode.rnode_length = len(RNode.rnode) if RNode.rnode else 0
            RNode.updating = False

        if RNode.updating:
            return
        else:
            threading.Thread(target=_update).start()


class Committee:

    committee = cf.cpc.getCommittees
    committee_length = len(committee) if committee else 0
    updating = False

    @staticmethod
    def update():
        def _update():
            Committee.updating = True
            Committee.committee = cf.cpc.getCommittees
            Committee.committee_length = len(committee) if committee else 0
            Committee.updating = False

        if Committee.updating:
            return
        else:
            threading.Thread(target=_update).start()


def explorer(request):
    height = block_collection.find().sort('_id', DESCENDING).limit(1)[0]['number']
    b_li = list(block_collection.find({'number': {'$lte': height}}).sort('number', DESCENDING).limit(20))[::-1]
    t_li = list(txs_collection.find().sort('timestamp', DESCENDING).limit(20))[::-1]

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
        now_ts = now - (i + 1) * DAY_SECENDS
        time_local = time.localtime(now_ts)
        dt = time.strftime('%m/%d', time_local)
        txs_day = txs_collection.find({'timestamp': {'$gte': gt_time, '$lt': lt_time}}).count()
        add_day = address_collection.find({'timestamp': {'$gte': gt_time, '$lt': lt_time}}).count()
        chart.append({'time': dt, 'tx': txs_day, 'bk': add_day})
    chart.reverse()

    # blocks
    blocks = []
    for b in b_li:
        block = {
            'id': b['number'],
            'reward': 5,
            'txs': len(b['transactions']),
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
            'amount': format(t['txfee'] , '.10f')
        }
        txs.append(tx)
    txs_count = txs_collection.find().count()
    header = {
        'blockHeight': height,
        'txs': txs_count,
        'rnode': RNode.rnode_length,
        'tps': get_tps(txs_count),
        'committee': Committee.committee_length,
    }

    return render(request, 'explorer/explorer.html',
                  {'blocks': blocks, 'txs': json.dumps(txs), 'chart': chart, 'header': header})


def wshandler(req):
    # index websocket handler
    uwsgi.websocket_handshake()
    temp_height = block_collection.find().sort('_id', DESCENDING).limit(1)[0]['number']
    while True:
        block = block_collection.find().sort('_id', DESCENDING).limit(1)[0]
        block_height = block['number']
        if block_height >= temp_height:
            RNode.update()
            Committee.update()
            txs_count = txs_collection.find().count()
            data = {}
            tps = get_tps(txs_count)
            header = {
                'blockHeight': block_height,
                'txs': txs_count,
                'rnode': RNode.rnode_length,
                'tps': tps,
                'committee': Committee.committee_length,
            }

            temp_block = block_collection.find({'number': temp_height})[0]
            block = {
                'id': temp_height,
                'reward': 5,
                'txs': len(temp_block['transactions']),
                'producerID': temp_block['miner'],
                'timestamp': temp_block['timestamp'],
                'hash': temp_block['hash'],
            }
            t_li = list(txs_collection.find().sort('timestamp', DESCENDING).limit(20))[::-1]
            txs = []
            for t in t_li:
                tx = {
                    'hash': t['hash'],
                    'sellerID': t['from'],
                    'buyerID': t['to'],
                    'timestamp': t['timestamp'],
                    'amount': format(t['txfee'] , '.10f')
                }
                txs.append(tx)
            data['header'] = header
            data['block'] = block
            data['txs'] = txs
            data = json.dumps(data)
            uwsgi.websocket_send(data)
            temp_height += 1
        else:
            time.sleep(REFRESH_INTERVAL)


def get_tps(txs_count):
    start_timestamp = block_collection.find({'number': 1})[0]['timestamp']
    current_timestamp = int(time.time())
    spend_time = current_timestamp - start_timestamp
    return round(txs_count / spend_time, 3)


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
            return render(req, 'explorer/search404.html')
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
                return render(req, 'explorer/search404.html')


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
    timesince = int(time.time()) - timestamp

    txs = len(block_dict['transactions'])
    miner = block_dict['miner']
    size = block_dict['size']
    gasUsed = block_dict['gasUsed']
    gasLimit = block_dict['gasLimit']
    blockReward = 5
    extraData = block_dict['proofOfAuthorityData']
    ##produce time
    if height > 1:
        last_block = block_collection.find({'number': height - 1})[0]
        timeproduce = timestamp - last_block['timestamp']
    else:
        timeproduce = 0

    return render(req, 'explorer/block_info.html', locals())


def txs(req):
    # txs
    block = req.GET.get('block')
    if block == None:
        try:
            page = req.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        all_txs = list(txs_collection.find().sort('_id', DESCENDING))
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
    txs_count = len(txs_from_block)

    p = Paginator(txs_from_block, 25, request=req)
    txs = p.page(page)
    return render(req, 'explorer/txs_list.html', {'txs': txs, 'blockNumber': block,'txs_count':txs_count})

def tx(req, tx_hash):
    # tx from hash
    search = tx_hash.strip().lower()

    tx_dict = list(txs_collection.find({"hash": search}))[0]
    status = cf.cpc.getTransactionReceipt(search).status
    tx_dict['gasLimit'] = block_collection.find({'number': tx_dict['blockNumber']})[0]['gasLimit']
    tx_dict['gasPrice'] = format(tx_dict['gasPrice'] / 1e18, '.20f')
    tx_dict['txfee'] = format(tx_dict['txfee'], '.20f')
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

    # timesince calc
    timenow = int(time.time())
    for t in txs:
        t['timesince'] = timenow - t['timestamp']

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
        creator = txs[-1]['from']
        return render(req, 'explorer/contract.html', {'txs': txs,
                                                      'address': raw_address,
                                                      'balance': balance,
                                                      'txs_count': txs_count,
                                                      'code': code,
                                                      'creator':creator
                                                      })


def rnode(req):
    epoch = cf.cpc.getCurrentTerm
    rnodes = RNode.rnode
    return render(req, 'explorer/rnode.html', {'epoch': epoch,
                                               'rnodes': rnodes})


def committee(req):
    epoch = cf.cpc.getCurrentTerm
    round = cf.cpc.getCurrentView
    committees = Committee.committee

    return render(req, 'explorer/committee.html', locals())
