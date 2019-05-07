import json
import math
import time
from contextlib import contextmanager

import eth_abi
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from pure_pagination import PageNotAnInteger, Paginator
from pymongo import DESCENDING, MongoClient

from cpchain_test.config import cfg
from cpchain_test.settings import cf

mongo = cfg['db']['ip']
CLIENT = MongoClient(host=mongo, port=27017, maxPoolSize=200)
block_collection = CLIENT['cpchain']['blocks']
txs_collection = CLIENT['cpchain']['txs']
address_collection = CLIENT['cpchain']['address']
contract_collection = CLIENT['cpchain']['contract']
rnode_collection = CLIENT['cpchain']['rnode']
proposer_collection = CLIENT['cpchain']['proposer']
event_collection = CLIENT['cpchain']['event']
abi_collection = CLIENT['cpchain']['abi']
source_collection = CLIENT['cpchain']['source']
chart_collection = CLIENT['cpchain']['chart']
num_collection = CLIENT['cpchain']['num']

try:
    import uwsgi
except:
    print('running local, uwsgi not work..')

REFRESH_INTERVAL = 3
ADD_SIZE = 42

# config.ini

DAY_SECENDS = 60 * 60 * 24
proposer_start_timestamp = 1556448256

@contextmanager
def timer(name):
    start = time.time()
    yield
    print(f'[{name}] done in {time.time() - start:.2f} s')
# usage:
# with timer('123'):
#     xxxxx

def get_chart():
    try:
        return chart_collection.find()[0].get('chart', [])
    except Exception:
        return []


class RNode:
    try:
        rnode = list(rnode_collection.find(({'Address': {'$exists': True}})))
    except:
        rnode = None
    try:
        view = rnode_collection.find({'view': {'$exists': True}})[0]['view']
    except:
        view = 1
    try:
        term = rnode_collection.find({'term': {'$exists': True}})[0]['term']
    except:
        term = 0

    @staticmethod
    def update():
        try:
            RNode.rnode = list(rnode_collection.find(({'Address': {'$exists': True}})))
            RNode.view = rnode_collection.find_one({'view': {'$exists': True}})['view']
            RNode.term = rnode_collection.find_one({'term': {'$exists': True}})['term']
        except Exception as e:
            pass


class Committee:
    try:
        committee = list(proposer_collection.find())
    except:
        committee = None

    @staticmethod
    def update():
        try:
            Committee.committee = list(proposer_collection.find())
        except Exception as e:
            print('committee update error>>>>>', e)


def explorer(request):
    with timer('height'):
        height = block_collection.find().sort('number', DESCENDING).limit(1)[0]['number']
    with timer('b_li'):
        b_li = list(block_collection.find({'number': {'$lte': height}}).sort('number', DESCENDING).limit(20))[::-1]
    with timer('t_li'):
        t_li = list(txs_collection.find().sort('_id', DESCENDING).limit(20))[::-1]
    # blocks
    blocks = []
    with timer('for b in b_li'):
        for b in b_li:
            block = {
                'id': b['number'],
                'reward': b['reward'],
                'txs': len(b['transactions']),
                'producerID': b['miner'],
                'timestamp': b['timestamp'],
                'hash': b['hash'],
            }

            if b['miner'].endswith('000000'):
                block['impeach'] = True
                block['impeachProposer'] = b['impeachProposer']

            blocks.append(block)

    # txs
    with timer('for t in t_li'):
        txs = []
        for t in t_li:
            if t['to']:
                tx = {
                    'hash': t['hash'],
                    'sellerID': t['from'],
                    'buyerID': t['to'],
                    'timestamp': t['timestamp'],
                    'amount': format(t['txfee'], '.10f')
                }
            else:
                creator = cf.toChecksumAddress(t['from'])
                contract = contract_collection.find({'creator': creator})[0]['address']
                tx = {
                    'hash': t['hash'],
                    'sellerID': t['from'],
                    'buyerID': t['to'],
                    'contract': contract,
                    'timestamp': t['timestamp'],
                    'amount': format(t['txfee'], '.10f')
                }
            txs.append(tx)
    with timer('last'):

        txs_count = txs_collection.count_documents({})
        header = {
            'blockHeight': height,
            'txs': txs_count,
            'rnode': len(RNode.rnode) if RNode.rnode else 0,
            'bps': get_rate('bps'),
            'tps': get_rate('tps'),
            'committee': proposerFomatter(RNode.view),
            'proposer': str(Committee.committee[0]['TermLen']) if Committee.committee else 0,
        }
    return render(request, 'explorer/explorer.html',
                  {'blocks': json.dumps(blocks), 'txs': json.dumps(txs), 'chart': get_chart(), 'header': header})


def proposerFomatter(num):
    return "%d%s" % (num, "tsnrhtdd"[(math.floor(num / 10) % 10 != 1) * (num % 10 < 4) * num % 10::4])


def wshandler(req):
    # index websocket handler
    uwsgi.websocket_handshake()
    with timer('temp_height'):
        temp_height = block_collection.find().sort('number', DESCENDING).limit(1)[0]['number']
    while True:
        block = block_collection.find().sort('number', DESCENDING).limit(1)[0]
        block_height = block['number']
        if block_height >= temp_height:
            RNode.update()
            Committee.update()
            with timer('ws 2'):
                txs_count = txs_collection.find().count()
            with timer('ws 21'):

                data = {}
                tps = get_rate('tps')
                bps = get_rate('bps')
            with timer('ws 22'):
                header = {
                    'blockHeight': block_height,
                    'txs': txs_count,
                    'rnode': len(RNode.rnode) if RNode.rnode else 0,
                    'bps': bps,
                    'tps': tps,
                    'committee': proposerFomatter(RNode.view),
                    'proposer': str(Committee.committee[0]['TermLen']) if Committee.committee else 0,
                }

            with timer('ws 3'):
                temp_block = block_collection.find({'number': temp_height})[0]
                block = {
                    'id': temp_height,
                    'reward': temp_block['reward'],
                    'txs': len(temp_block['transactions']),
                    'producerID': temp_block['miner'],
                    'timestamp': temp_block['timestamp'],
                    'hash': temp_block['hash'],
                }
                if temp_block['miner'].endswith('000000'):
                    block['impeach'] = True
                    block['impeachProposer'] = temp_block['impeachProposer']
                t_li = list(txs_collection.find().sort('timestamp', DESCENDING).limit(20))[::-1]
                txs = []
            for t in t_li:
                if t['to']:
                    tx = {
                        'hash': t['hash'],
                        'sellerID': t['from'],
                        'buyerID': t['to'],
                        'timestamp': t['timestamp'],
                        'amount': format(t['txfee'], '.10f')
                    }
                else:
                    creator = cf.toChecksumAddress(t['from'])
                    contract = contract_collection.find({'creator': creator})[0]['address']
                    tx = {
                        'hash': t['hash'],
                        'sellerID': t['from'],
                        'buyerID': t['to'],
                        'contract': contract,
                        'timestamp': t['timestamp'],
                        'amount': format(t['txfee'], '.10f')
                    }
                txs.append(tx)
            with timer('ws last'):
                data['header'] = header
                data['block'] = block
                data['txs'] = txs
                data = json.dumps(data)
                uwsgi.websocket_send(data)
                temp_height += 1
                time.sleep(0.2)
        else:
            time.sleep(REFRESH_INTERVAL)


def get_rate(bORt):
    if bORt == 'tps':
        return num_collection.find({'type': 'tps'})[0].get('tps')
    elif bORt == 'bps':
        return num_collection.find({'type': 'bps'})[0].get('bps')


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
    all_blocks = block_collection.find().sort('number', DESCENDING)
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
    blockReward = block_dict['reward']
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
        all_txs = txs_collection.find().sort('_id', DESCENDING)
        p = Paginator(all_txs, 25, request=req)
        txs = p.page(page)
        txs.object_list = list(txs.object_list)
        for tx in txs.object_list:
            if not tx['to']:
                tx['contract'] = contract_collection.find({'txhash': tx['hash']})[0]['address']
            tx['value'] = cf.fromWei(tx['value'], 'ether')
        return render(req, 'explorer/txs_list.html', {'txs': txs})
    # block's type is string
    txs_from_block = txs_collection.find({'blockNumber': int(block)})
    # page
    try:
        page = req.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    txs_count = txs_from_block.count()

    p = Paginator(txs_from_block, 25, request=req)
    txs = p.page(page)
    txs.object_list = list(txs.object_list)
    for tx in txs.object_list:
        if not tx['to']:
            tx['contract'] = contract_collection.find({'txhash': tx['hash']})[0]['address']
        tx['value'] = cf.fromWei(tx['value'], 'ether')
    return render(req, 'explorer/txs_list.html', {'txs': txs,
                                                  'blockNumber': block,
                                                  'txs_count': txs_count
                                                  })


def tx(req, tx_hash):
    # tx from hash
    search = tx_hash.strip().lower()

    tx_dict = list(txs_collection.find({"hash": search}))[0]
    tx_dict['gasLimit'] = block_collection.find({'number': tx_dict['blockNumber']})[0]['gasLimit']
    tx_dict['gasPrice'] = format(tx_dict['gasPrice'] / 1e18, '.20f')
    tx_dict['txfee'] = format(tx_dict['txfee'], '.20f')
    tx_dict['value'] = cf.fromWei(tx_dict['value'], 'ether')
    if not tx_dict['to']:
        contract = contract_collection.find({'txhash': tx_hash})[0]['address']
        return render(req, 'explorer/tx_info.html', {'tx_dict': tx_dict, 'contract': contract})
    return render(req, 'explorer/tx_info.html', {'tx_dict': tx_dict})


def address(req, address):
    try:
        raw_address = cf.toChecksumAddress(address.strip())
        address = raw_address.lower()
        code = contract_collection.find({'address': raw_address})[0]['code']
        code = cf.toHex(code)
    except Exception as e:
        code = '0x'
    # address info
    txs = txs_collection.find({'$or': [{'from': address}, {'to': address}]}).sort('timestamp', -1)
    txs_count = txs.count()
    txs = list(txs[:25])
    timenow = int(time.time())
    # set flag
    for d in txs:
        if d['from'] == d['to']:
            d['flag'] = 'self'
        elif d['from'] == address:
            d['flag'] = 'out'
        else:
            d['flag'] = 'in'
        # add contract address
        if not d['to']:
            d['contract'] = contract_collection.find({'txhash': d['hash']})[0]['address']
        d['value'] = cf.fromWei(d['value'], 'ether')
        d['timesince'] = timenow - d['timestamp']

    # txs.sort(key=lambda x: x['timestamp'], reverse=True)

    try:
        balance = cf.fromWei(cf.cpc.getBalance(raw_address), 'ether')
    except:
        print('cf connection error')
        balance = 0

    # latest 25 txs

    if code == '0x':
        proposer_history = block_collection.count_documents({'miner': address, "timestamp": {'$gt': proposer_start_timestamp}})
        return render(req, 'explorer/address.html', {'txs': txs,
                                                     'address': raw_address,
                                                     'balance': balance,
                                                     'txs_count': txs_count,
                                                     'proposer_history': proposer_history
                                                     })
    else:
        creator = contract_collection.find({'address': raw_address})[0]['creator']
        return render(req, 'explorer/contract.html', {'txs': txs,
                                                      'address': raw_address,
                                                      'balance': balance,
                                                      'txs_count': txs_count,
                                                      'code': code,
                                                      'creator': creator,
                                                      })


def rnode(req):
    epoch = RNode.term
    rnodes = RNode.rnode
    try:
        rnodes.sort(key=lambda d: d['Rpt'], reverse=True)
    except Exception:
        pass
    return render(req, 'explorer/rnode.html', {'epoch': epoch,
                                               'rnodes': rnodes})


def committee(req):
    proposerlist = list(proposer_collection.find())[0]
    term = proposerlist.get('Term', [])
    view = proposerlist.get('View', [])
    TermLen = proposerlist['TermLen'] if proposerlist else 1
    BlockNumber = proposerlist['BlockNumber'] if proposerlist else 1
    proposers = proposerlist.get('Proposers', [])

    return render(req, 'explorer/Proposer.html', locals())


def event(req, address):
    address = cf.toChecksumAddress(address.strip())
    events = list(event_collection.find({'contract_address': address}, {'_id': 0, 'contract_address': 0}))
    queryset = abi_collection.find({'contract_address': address}, {'_id': 0, 'contract_address': 0})
    if queryset.count() > 0:
        event_abi = queryset[0]['event_abi']
        events = decode_event(event_abi, events)

    return JsonResponse({"status": 1, "message": 'success', "data": events})


def decode_event(event_abi, event_list):
    events = []
    for e in event_list:
        topics = e['topics']
        data = e['data']
        event = event_abi[topics[0]]
        values = eth_abi.decode_abi(event['arg_types'], cf.toBytes(hexstr=data))
        event_name = event['event_name']
        events.append({
            'topics': topics,
            'data': data,
            'name': event_name,
            'arg_types': event['arg_types'],
            'arg_values': values
        })

    return events


def parse_event_abi(contract_abi):
    event_abi = {}
    for f in contract_abi:
        if f['type'] == 'event':
            event_name = f['name']
            topic = f['signature']
            arg_types = [i['type'] for i in f['inputs']]
            arg_names = [i['name'] for i in f['inputs']]

            event_abi[topic] = {
                'event_name': event_name,
                'arg_types': arg_types,
                'arg_names': arg_names,
            }
    return event_abi


def abi(req, address):
    address = cf.toChecksumAddress(address.strip())
    if req.method == 'GET':
        queryset = abi_collection.find({'contract_address': address}, {'_id': 0, 'contract_address': 0})
        if queryset.count() == 0:
            return JsonResponse({"status": 0, "message": 'no abi found'})
        abi = list(queryset)
        return JsonResponse({"status": 1, "message": 'success', "data": abi})
    elif req.method == 'POST':
        abi = req.POST.get('abi')
        try:
            abi = json.loads(abi)
        except:
            return JsonResponse({"status": 0, "message": 'wrong abi'})

        if abi_collection.find({'contract_address': address}).count() != 0:
            return JsonResponse({"status": 0, "message": 'duplicated request'})

        event_abi = parse_event_abi(abi)
        abi_collection.insert_one(
            {
                'contract_address': address,
                'abi': abi,
                'event_abi': event_abi,
            })

        return JsonResponse({"status": 1, "message": 'success'})


def source(req, address):
    address = cf.toChecksumAddress(address.strip())
    if req.method == 'GET':
        queryset = source_collection.find({'contract_address': address}, {'_id': 0, 'contract_address': 0})
        if queryset.count() == 0:
            return JsonResponse({"status": 0, "message": 'no source found'})
        source = list(queryset)
        return JsonResponse({"status": 1, "message": 'success', "data": source})
    elif req.method == 'POST':
        source = req.POST.get('source')

        # TODO: source verification

        if source_collection.find({'contract_address': address}).count() != 0:
            return JsonResponse({"status": 0, "message": 'duplicated request'})

        source_collection.insert_one(
            {
                'contract_address': address,
                'source': source,
            })
        return JsonResponse({"status": 1, "message": 'success'})
