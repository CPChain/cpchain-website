import json
import math
import time
from contextlib import contextmanager

import eth_abi
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from pure_pagination import PageNotAnInteger, Paginator
from pymongo import DESCENDING, MongoClient, ASCENDING

from apps.utils import currency
from cpchain_test.config import cfg
from cpchain_test.settings import cf
from . import withdraw_abi

mongo = cfg['db']['ip']
CLIENT = MongoClient(host=mongo, port=27017, maxPoolSize=200)
block_collection = CLIENT['cpchain']['blocks']
txs_collection = CLIENT['cpchain']['txs']
address_collection = CLIENT['cpchain']['address']
contract_collection = CLIENT['cpchain']['contract']
rnode_collection = CLIENT['cpchain']['rnode']
proposer_collection = CLIENT['cpchain']['proposer']
proposer_history_collection = CLIENT['cpchain']['proposer_history']
event_collection = CLIENT['cpchain']['event']
abi_collection = CLIENT['cpchain']['abi']
source_collection = CLIENT['cpchain']['source']
chart_collection = CLIENT['cpchain']['chart']
num_collection = CLIENT['cpchain']['num']

REFRESH_INTERVAL = 3
ADD_SIZE = 42

# config.ini

DAY_SECENDS = 60 * 60 * 24
proposer_start_timestamp = 1556448256


# usage:
# with timer('123'):
#     xxxxx
@contextmanager
def timer(name):
    start = time.time()
    yield
    print(f'[{name}] done in {time.time() - start:.2f} s')


def get_chart():
    try:
        return chart_collection.find()[0].get('chart', [])
    except Exception:
        return []


def explorer(request):
    height = block_collection.find().sort('number', DESCENDING).limit(1)[0]['number']
    b_li = list(block_collection.find({'number': {'$lte': height}}).sort('number', DESCENDING).limit(20))[::-1]
    t_li = list(txs_collection.find().sort('_id', DESCENDING).limit(20))[::-1]
    # blocks
    blocks = []
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
    txs_count = txs_collection.find().count()
    try:
        view = rnode_collection.find({'view': {'$exists': True}})[0]['view']
    except:
        view = 1
    header = {
        'blockHeight': height,
        'txs': txs_count,
        'rnode': rnode_collection.find(({'Address': {'$exists': True}})).count(),
        'bps': get_rate('bps'),
        'tps': get_rate('tps'),
        'committee': proposerFomatter(view),
        'proposer': len(list(proposer_collection.find())[0].get('Proposers', []))
    }
    return render(request, 'explorer/explorer.html',
                  {'blocks': json.dumps(blocks), 'txs': json.dumps(txs), 'chart': get_chart(), 'header': header})


def proposerFomatter(num):
    return "%d%s" % (num, "tsnrhtdd"[(math.floor(num / 10) % 10 != 1) * (num % 10 < 4) * num % 10::4])


def wshandler():
    # index websocket handler
    block = block_collection.find().sort('number', DESCENDING).limit(1)[0]
    block_height = block['number']
    txs_count = txs_collection.find().count()
    tps = get_rate('tps')
    bps = get_rate('bps')
    try:
        view = rnode_collection.find({'view': {'$exists': True}})[0]['view']
    except:
        view = 1

    header = {
        'blockHeight': block_height,
        'txs': txs_count,
        'rnode': rnode_collection.find(({'Address': {'$exists': True}})).count(),
        'bps': bps,
        'tps': tps,
        'committee': proposerFomatter(view),
        # 'proposer': str(Committee.committee[0]['TermLen']) if Committee.committee else 0,
        'proposer': len(list(proposer_collection.find())[0].get('Proposers', []))
    }
    new_block = {
        'id': block_height,
        'reward': block['reward'],
        'txs': len(block['transactions']),
        'producerID': block['miner'],
        'timestamp': block['timestamp'],
        'hash': block['hash'],
    }
    if block['miner'].endswith('000000'):
        new_block['impeach'] = True
        new_block['impeachProposer'] = block['impeachProposer']

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
    data = {}
    data['header'] = header
    data['block'] = new_block
    data['txs'] = txs
    return data


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


def searchproposer(req):
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
    blocks.object_list = list(blocks.object_list)
    for b in blocks.object_list:
        if b['miner'].endswith('000000'):
            b['impeach'] = True
        else:
            b['impeach'] = False
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
            tx['value'] = currency.from_wei(tx['value'], 'ether')
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
        tx['value'] = currency.from_wei(tx['value'], 'ether')
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
    tx_dict['value'] = currency.from_wei(tx_dict['value'], 'ether')
    if not tx_dict['to']:
        contract = contract_collection.find({'txhash': tx_hash})[0]['address']
        return render(req, 'explorer/tx_info.html', {'tx_dict': tx_dict, 'contract': contract})
    return render(req, 'explorer/tx_info.html', {'tx_dict': tx_dict})


def address(req, address):
    with timer('all'):
        try:
            raw_address = cf.toChecksumAddress(address.strip())
            address = raw_address.lower()
            code = contract_collection.find({'address': raw_address})[0]['code']
            # code = cf.toHex(code)
        except Exception as e:
            code = '0x'
        # address info
        txs = txs_collection.find({'$or': [{'from': address}, {'to': address}]}).sort('timestamp', DESCENDING)
        txs_count = txs.count()

        try:
            page = req.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(txs, 25, request=req)
        txs = p.page(page)
        txs.object_list = list(txs.object_list)

        timenow = int(time.time())
        # set flag
        for d in txs.object_list:
            if d['from'] == d['to']:
                d['flag'] = 'self'
            elif d['from'] == address:
                d['flag'] = 'out'
            else:
                d['flag'] = 'in'
            # add contract address
            if not d['to']:
                d['contract'] = contract_collection.find({'txhash': d['hash']})[0]['address']
            d['value'] = currency.from_wei(d['value'], 'ether')
            d['timesince'] = timenow - d['timestamp']

        # txs.sort(key=lambda x: x['timestamp'], reverse=True)

        try:
            balance = currency.from_wei(cf.cpc.getBalance(raw_address), 'ether')
        except:
            print('cf connection error')
            balance = 0

        # latest 25 txs
        current = {'begin': (int(page) - 1) * 25 + 1, 'end': (int(page) - 1) * 25 + len(txs.object_list)}
        # current =1
        if code == '0x':
            proposer_history = block_collection.count(
                {'miner': address, "timestamp": {'$gt': proposer_start_timestamp}})
            return render(req, 'explorer/address.html', {'txs': txs, 'current': current,
                                                         'address': raw_address,
                                                         'balance': balance,
                                                         'txs_count': txs_count,
                                                         'proposer_history': proposer_history
                                                         })
        else:
            creator = contract_collection.find({'address': raw_address})[0]['creator']
            return render(req, 'explorer/contract.html', {'txs': txs, 'current': current,
                                                          'address': raw_address,
                                                          'balance': balance,
                                                          'txs_count': txs_count,
                                                          'code': code,
                                                          'creator': creator,
                                                          })


def rnode(req):
    term = list(proposer_collection.find())[0].get('Term', [])
    rnodes = list(rnode_collection.find(({'Address': {'$exists': True}})))
    try:
        rnodes.sort(key=lambda d: d['Rpt'], reverse=True)
    except Exception:
        pass
    return render(req, 'explorer/rnode.html', {'term': term,
                                               'rnodes': rnodes})


def proposers(req):
    proposerlist = list(proposer_collection.find())[0]
    term = proposerlist.get('Term', [])
    view = int(proposerlist.get('View', [])) + 1
    TermLen = proposerlist['TermLen'] if proposerlist else 1
    BlockNumber = proposerlist['BlockNumber'] if proposerlist else 1
    proposers = proposerlist.get('Proposers', [])
    return render(req, 'explorer/Proposer.html', locals())


def committeeHistory(req):
    all_historys = proposer_history_collection.find().sort('Term', -1)
    try:
        page = req.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(all_historys, 3, request=req)
    historys = p.page(page)
    historys.object_list = list(historys.object_list)

    return render(req, 'explorer/ProposerHistory.html', {'historys': historys})


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


def impeachs_by_addr(req, address):
    address = address.strip()
    if not cf.isAddress(address):
        return HttpResponse('invalid address.')
    address = cf.toChecksumAddress(address).lower()
    impeach_bks = block_collection.find({'impeachProposer': address}, {'_id': 0}).sort('number', DESCENDING)
    res = {}
    res['impeach_num'] = impeach_bks.count()
    res['success_num'] = block_collection.find({'miner': address}).count()
    res['impeach_bks'] = list(impeach_bks)
    return JsonResponse(res, safe=False)


def impeachs_by_block(req, block, isOur):
    block = int(block)

    if isOur == '0':
        impeach_bks = block_collection.find(
            {'number': {'$gt': block}, 'impeachProposer': {'$exists': True}},
            {'_id': False})
    elif isOur == '1':
        impeach_bks = block_collection.find(
            {'number': {'$gt': block}, 'impeachProposer': {'$exists': True},
             'impeachProposer': {'$in': withdraw_abi.ours}},
            {'_id': False})
    res = {}
    res['impeach_num'] = impeach_bks.count()
    res['impeach_bks'] = list(impeach_bks)
    return JsonResponse(res)


def all_blocks(req):
    height = block_collection.find().sort('number', DESCENDING).limit(1)[0]['number']
    height = int(height)
    blocks = block_collection.find({'number': {'$gt': (height - 1000)}},
                                   {'_id': False, 'transactions': False}).sort('number', DESCENDING)
    res = {}
    res['latest_1000_blocks'] = list(blocks)
    return JsonResponse(res)


def check_campaign(req):
    config = withdraw_abi.config
    # from cpc_fusion import Web3
    # provider = "http://45.56.121.119:8601"
    # test_cf = Web3(Web3.HTTPProvider(provider))
    campaign = cf.cpc.contract(abi=config["abi"], address="0x20BF49A0773a2b9eA5cF218C188d7F633b07c267")

    term = campaign.functions.termIdx().call()
    ten_candidates = []
    min = term - 10 if term - 10 >= 0 else 0
    for i in range(min, term):
        candidates = campaign.functions.candidatesOf(i).call()
        # for c in candidates:
        #     print(campaign.functions.candidateInfoOf(c).call())
        candidates = [c.lower() + ' *' if c.lower() in withdraw_abi.ours else c.lower() for c in candidates]

        ten_candidates.append({'term': i, 'candidates': candidates})
    ten_candidates = ten_candidates[::-1]

    return render(req, 'explorer/campaign.html', locals())


def candidate_info(req, addr):
    config = withdraw_abi.config
    campaign = cf.cpc.contract(abi=config["abi"], address="0xb8A07aE42E2902C41336A301C22b6e849eDd4F8B")
    if addr.endswith(' *'):
        addr = addr[:-2]

    addr = cf.toChecksumAddress(addr)
    info = campaign.functions.candidateInfoOf(addr).call()
    return JsonResponse(info, safe=False)


def impeachFrequency(req):
    now = int(time.time())
    day_zero = now - now % DAY_SECENDS
    chart = []
    for i in range(30):
        gt_time = day_zero - (i + 1) * DAY_SECENDS
        lt_time = day_zero - i * DAY_SECENDS
        our_impeachs = block_collection.find(
            {'timestamp': {'$gte': gt_time, '$lt': lt_time}, 'impeachProposer': {'$exists': True},
             'impeachProposer': {'$in': withdraw_abi.ours}}, {'_id': False}).count()
        all_impeachs = block_collection.find(
            {'timestamp': {'$gte': gt_time, '$lt': lt_time}, 'impeachProposer': {'$exists': True}}).count()
        com_impeachs = all_impeachs - our_impeachs
        our_success = block_collection.find(
            {'timestamp': {'$gte': gt_time, '$lt': lt_time}, 'impeachProposer': {'$exists': False},
             'miner': {'$in': withdraw_abi.ours}}).count()
        com_success = block_collection.find(
            {'timestamp': {'$gte': gt_time, '$lt': lt_time}}).count() - all_impeachs - our_success
        try:
            our_impeach_frequency = our_impeachs / our_success
        except:
            our_impeach_frequency = 0
        try:
            com_impeach_frequency = com_impeachs / com_success
        except:
            com_impeach_frequency = 0
        now_ts = now - (i + 1) * DAY_SECENDS
        time_local = time.localtime(now_ts)
        dt = time.strftime('%m/%d', time_local)
        chart.append({
            'our_impeachs': -our_impeachs,
            'our_success': our_success,
            'com_impeachs': -com_impeachs,
            'com_success': com_success,
            'our_impeach_frequency': our_impeach_frequency,
            'com_impeach_frequency': com_impeach_frequency,
            'date': str(dt)
        })
    chart.reverse()
    # today impeach
    our_impeachs = block_collection.find(
        {'timestamp': {'$gte': day_zero}, 'impeachProposer': {'$exists': True},
         'impeachProposer': {'$in': withdraw_abi.ours}}, {'_id': False}).count()
    all_impeachs = block_collection.find(
        {'timestamp': {'$gte': day_zero}, 'impeachProposer': {'$exists': True}}).count()
    com_impeachs = all_impeachs - our_impeachs
    our_success = block_collection.find(
        {'timestamp': {'$gte': day_zero}, 'impeachProposer': {'$exists': False},
         'miner': {'$in': withdraw_abi.ours}}).count()
    com_success = block_collection.find(
        {'timestamp': {'$gte': day_zero}}).count() - all_impeachs - our_success
    try:
        our_impeach_frequency = our_impeachs / our_success
    except:
        our_impeach_frequency = 0
    try:
        com_impeach_frequency = com_impeachs / com_success
    except:
        com_impeach_frequency = 0

    chart.append({
        'our_impeachs': -our_impeachs,
        'our_success': our_success,
        'com_impeachs': -com_impeachs,
        'com_success': com_success,
        'our_impeach_frequency': our_impeach_frequency,
        'com_impeach_frequency': com_impeach_frequency,
        'date': 'today'
    })
    return render(req, 'explorer/impeachs.html', {'chart': chart})


def proposer_history(req, address):
    address = address.lower()
    blocks_by_proposer = block_collection.find(
        {'miner': address, "timestamp": {'$gt': proposer_start_timestamp}}).sort('number', DESCENDING)
    try:
        page = req.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(blocks_by_proposer, 25, request=req)
    blocks = p.page(page)
    blocks.object_list = list(blocks.object_list)
    blocks_count = blocks_by_proposer.count()
    current = {'begin': (int(page) - 1) * 25 + 1, 'end': (int(page) - 1) * 25 + len(blocks.object_list)}
    return render(req, 'explorer/proposer_history_list.html',
                  {'blocks': blocks, 'current': current, 'address': address, 'blocks_count': blocks_count})
