from django.http.response import Http404
from common.pageable import PageableBackend
import json
import math
import time
import csv
from datetime import datetime as dt

import eth_abi
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from pymongo import DESCENDING, MongoClient

from apps.utils import currency
from apps.utils.pure_pagination import PageNotAnInteger, Paginator
from apps.utils.update_our_proposer import read_our_proposer
from cpchain_test.config import cfg
from cpchain_test.settings import cf, NO_CHAIN_NODE
from . import withdraw_abi

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .filters import TxsQueryBackend

# from .models import AddressMark, AddressMarkType
# from .serializers import AddressMarkSerializer, AddressMarkTypeSerializer

from log import get_log

log = get_log('app')

our_proposer = read_our_proposer()
mongo = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])

REFRESH_INTERVAL = 3
ADD_SIZE = 42

# config.ini

DAY_SECENDS = 60 * 60 * 24
proposer_start_timestamp = 1556448256

CLIENT = MongoClient(host=mongo, port=port, maxPoolSize=200)
uname = cfg['mongo']['uname']
pwd = cfg['mongo']['password']
db = CLIENT['cpchain']
db.authenticate(uname, pwd)

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


def get_chart():
    try:
        # TODO 目前 chart 中存储的是序列化后的字符串，需改为数组，改掉后，本处也将修改
        return chart_collection.find()[0].get('chart', [])
    except Exception:
        return []


def explorerDev(request):
    try:
        height = block_collection.find().sort(
            'number', DESCENDING).limit(1)[0]['number']
    except IndexError as e:
        print(e)
        blocks = []
        txs = []
        header = {'blockHeight': 0,
                  'txs': 0,
                  'rnode': 0,
                  'bps': 0,
                  'tps': 0,
                  'committee': '0/0',
                  'proposer': 0, }
        return render(request, 'explorer/explorer.html',
                      {'blocks': json.dumps(blocks), 'txs': json.dumps(txs), 'chart': get_chart(), 'header': header})
    b_li = list(block_collection.find({'number': {'$lte': height}}).sort(
        'number', DESCENDING).limit(20))[::-1]
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
            contract = contract_collection.find(
                {'creator': creator})[0]['address']
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
        index = proposer_collection.find({'ProposerIndex': {'$exists': True}})[
            0]['ProposerIndex'] + 1
    except:
        index = 1
    header = {
        'blockHeight': height,
        'txs': txs_count,
        'rnode': rnode_collection.find(({'Address': {'$exists': True}})).count(),
        'bps': get_rate('bps'),
        'tps': get_rate('tps'),
        'committee': proposerFomatter(index),
        'proposer': len(list(proposer_collection.find())[0].get('Proposers', []))
    }

    return render(request, 'explorer/explorer.html',
                  {'blocks': json.dumps(blocks), 'txs': json.dumps(txs), 'chart': get_chart(), 'header': header})


class ExplorerDashboardView(viewsets.ViewSet):

    def list(self, request):
        try:
            height = block_collection.find().sort(
                'number', DESCENDING).limit(1)[0]['number']
        except IndexError as e:
            print(e)
            header = {'blockHeight': 0,
                      'txs': 0,
                      'rnode': 0,
                      'bps': 0,
                      'tps': 0,
                      'committee': '0/0',
                      'proposer': 0, }
            return Response({'blocks': [], 'txs': [], 'chart': get_chart(), 'header': header})
        b_li = list(block_collection.find({'number': {'$lte': height}}).sort(
            'number', DESCENDING).limit(20))[::-1]
        t_li = list(txs_collection.find().sort(
            '_id', DESCENDING).limit(20))[::-1]
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
                contract = contract_collection.find(
                    {'txhash': t['hash']})[0]['address']
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
            index = proposer_collection.find({'ProposerIndex': {'$exists': True}})[
                0]['ProposerIndex'] + 1
        except:
            index = 1
        header = {
            'blockHeight': height,
            'txs': txs_count,
            'rnode': rnode_collection.find(({'Address': {'$exists': True}})).count(),
            'bps': get_rate('bps'),
            'tps': get_rate('tps'),
            'committee': proposerFomatter(index),
            'proposer': len(list(proposer_collection.find())[0].get('Proposers', []))
        }
        return Response({'blocks': blocks, 'txs': txs, 'chart': get_chart(), 'header': header})


def explorer(request):
    try:
        height = block_collection.find().sort(
            'number', DESCENDING).limit(1)[0]['number']
    except IndexError as e:
        print(e)
        blocks = []
        txs = []
        header = {'blockHeight': 0,
                  'txs': 0,
                  'rnode': 0,
                  'bps': 0,
                  'tps': 0,
                  'committee': '0/0',
                  'proposer': 0, }
        return render(request, 'explorer/explorer.html',
                      {'blocks': json.dumps(blocks), 'txs': json.dumps(txs), 'chart': get_chart(), 'header': header})
    b_li = list(block_collection.find({'number': {'$lte': height}}).sort(
        'number', DESCENDING).limit(20))[::-1]
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
            contract = contract_collection.find(
                {'txhash': t['hash']})[0]['address']
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
        index = proposer_collection.find({'ProposerIndex': {'$exists': True}})[
            0]['ProposerIndex'] + 1
    except:
        index = 1
    header = {
        'blockHeight': height,
        'txs': txs_count,
        'rnode': rnode_collection.find(({'Address': {'$exists': True}})).count(),
        'bps': get_rate('bps'),
        'tps': get_rate('tps'),
        'committee': proposerFomatter(index),
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
        index = proposer_collection.find({'ProposerIndex': {'$exists': True}})[
            0]['ProposerIndex'] + 1
    except:
        index = 1

    header = {
        'blockHeight': block_height,
        'txs': txs_count,
        'rnode': rnode_collection.find(({'Address': {'$exists': True}})).count(),
        'bps': bps,
        'tps': tps,
        'committee': proposerFomatter(index),
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

    t_li = list(txs_collection.find().sort(
        'timestamp', DESCENDING).limit(20))[::-1]
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
            contract = contract_collection.find(
                {'txhash': t['hash']})[0]['address']
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
    try:
        if bORt == 'tps':
            return num_collection.find({'type': 'tps'})[0].get('tps')
        elif bORt == 'bps':
            return num_collection.find({'type': 'bps'})[0].get('bps')
    except Exception as e:
        print(e)
        return 0


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


class BlocksView(viewsets.ViewSet):
    filter_backends = [PageableBackend, ]

    def list(self, request):
        results = []
        count = 0
        page = 1
        try:
            # blocks
            all_blocks = block_collection.find(
                projection={'_id': False, 'dpor': False}).sort('number', DESCENDING)
            count = block_collection.estimated_document_count()
            limit = min(int(request.GET.get('limit', 25)), 100)
            page = int(request.GET.get('page', 1))
            p = Paginator(all_blocks, limit, request=request)
            blocks = p.page(page)
            blocks.object_list = list(blocks.object_list)
            for b in blocks.object_list:
                if b['miner'].endswith('000000'):
                    b['impeach'] = True
                else:
                    b['impeach'] = False
                b['txs_cnt'] = len(b['transactions'])
                del b['transactions']
            results = blocks.object_list
        except Exception as e:
            log.error(e)
        return Response({'results': results, 'count': count, 'page': page})

    def retrieve(self, request, pk):
        """ 通过指定 Number 或 Hash 获取区块信息
        """
        search = pk.strip().lower()
        filters = {}
        if len(search) < ADD_SIZE - 2:
            # search by number
            filters = {'number': int(search)}
        else:
            if not search.startswith('0x'):
                search = '0x' + search
            filters = {"hash": search}
        if block_collection.count_documents(filters) == 0:
            return Response({"error": "not found"}, status=404)
        block_dict = block_collection.find(
            filters, projection={'_id': False})[0]
        block_dict['txs_cnt'] = len(block_dict['transactions'])
        del block_dict['transactions']
        block_dict['transactions'] = []
        if block_dict['txs_cnt'] > 0:
            txs_from_block = txs_collection.find(
                {'blockNumber': int(block_dict['number'])}, projection={'_id': False})
            txs = []
            for tx in txs_from_block:
                if not tx['to']:
                    tx['contract_address'] = contract_collection.find(
                        {'txhash': tx['hash']})[0]['address']
                tx['value'] = currency.from_wei(tx['value'], 'ether')
                txs.append(tx)
            block_dict['transactions'] = txs
        return Response(block_dict)


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

    extraData = block_dict.get(
        'extraData', block_dict.get('proofOfAuthorityData'))
    # produce time
    if height > 1:
        last_block = block_collection.find({'number': height - 1})[0]
        timeproduce = timestamp - last_block['timestamp']
    else:
        timeproduce = 0

    return render(req, 'explorer/block_info.html', locals())


def parse_txs_filter(request):
    address = request.GET.get('address', None)
    filters = {}
    address_filter = None
    # address
    if address is not None:
        if not address.startswith('0x'):
            address = "0x" + address
        address = cf.toChecksumAddress(address.strip()).lower()
        address_filter = {'$or': [{'from': address}, {'to': address}]}
        flag = request.GET.get('type')
        if flag == 'in':
            address_filter = {'to': address}
        elif flag == 'out':
            address_filter = {'from': address}

    # 是否排除交易额为 0 的交易
    exclude_empty_value = request.GET.get('exclude_value_0', False)
    exclude_empty_value_filter = None
    if exclude_empty_value:
        exclude_empty_value_filter = {'value': {'$ne': 0.0}}

    # TODO 暂不支持
    # exclude_contract = request.GET.get('exclude_contract', False)
    # exclude_contract_filter = None
    # if exclude_contract:
    #     exclude_contract_filter = {'isContract': False}

    block_number = request.GET.get('block_number', None)
    block_number_filter = None
    try:
        block_number = int(block_number)
        if block_number >= 0:
            block_number_filter = {'blockNumber': block_number}
    except Exception:
        pass

    block_hash = request.GET.get('block_hash', False)
    block_hash_filter = None
    if block_hash:
        block_hash_filter = {'blockHash': block_hash}

    # date range
    data_range_filter = None
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    if start_date:
        start_at = dt.strptime(start_date, '%Y-%m-%d').timestamp()
        end_at = dt.now().timestamp()
        if end_date:
            end_at = dt.strptime(end_date, '%Y-%m-%d').timestamp()
        if (end_at - start_at) > 1 * 30 * 24 * 3600:
            raise Exception("Date range can't greater than 1 month")
        data_range_filter = {
            "timestamp": {
                "$gt": start_at,
                "$lt": end_at
            }
        }

    filters_list = [address_filter,
                    exclude_empty_value_filter, block_number_filter, block_hash_filter, data_range_filter]
    filters_list = [i for i in filters_list if i is not None]
    if len(filters_list) > 0:
        filters = {"$and": filters_list}

    return filters


class TxsView(viewsets.ViewSet):
    filter_backends = [PageableBackend, TxsQueryBackend]

    def list(self, request):
        results = []
        count = 0
        page = 1
        limit = 25
        try:
            # query filters
            filters = parse_txs_filter(request)
            # blocks
            all_txs = txs_collection.find(
                filters, projection={'_id': False}).sort('_id', DESCENDING)
            count = txs_collection.count(filters)
            limit = min(int(request.GET.get('limit', 25)), 50)
            page = int(request.GET.get('page', 1))
            p = Paginator(all_txs, limit, request=request)
            txs = p.page(page)
            txs.object_list = list(txs.object_list)
            for tx in txs.object_list:
                if not tx['to']:
                    tx['contract'] = contract_collection.find(
                        {'txhash': tx['hash']})[0]['address']
                tx['value'] = currency.from_wei(tx['value'], 'ether')
            results = txs.object_list
        except Exception as e:
            log.error(e)
        return Response({'results': results, 'count': count, 'page': page, 'limit': limit})

    def retrieve(self, request, pk):
        """ 根据 hash 获取交易
        """
        search = pk.strip().lower()
        filters = {}
        if not search.startswith('0x'):
            search = '0x' + search
        filters = {"hash": search}
        if txs_collection.count_documents(filters) == 0:
            return Response({"error": "not found"}, status=404)
        tx_dict = txs_collection.find(filters, projection={'_id': False})[0]
        tx_dict['gasLimit'] = block_collection.find(
            {'number': tx_dict['blockNumber']})[0]['gasLimit']
        tx_dict['gasPrice'] = format(tx_dict['gasPrice'] / 1e18, '.20f')
        tx_dict['txfee'] = format(tx_dict['txfee'], '.20f')
        tx_dict['value'] = currency.from_wei(tx_dict['value'], 'ether')
        try:
            input_data = cf.toText(hexstr=tx_dict['input'])
            input_data = input_data.replace('\\', r'\\')
            input_data = input_data.replace('`', r'\`')
        except Exception as e:
            input_data = tx_dict['input']

        tx_dict['input_data'] = input_data

        if not tx_dict['to']:
            tx_dict['contract_address'] = contract_collection.find(
                {'txhash': search}, projection={'_id': False})[0]['address']

        return Response(tx_dict)


class ExportTxsView(viewsets.ViewSet):
    filter_backends = [PageableBackend, TxsQueryBackend]

    def list(self, request):
        results = []
        address = request.GET.get('address')
        if not address:
            raise Exception('address can not be None')
        start_date = request.GET.get('start_date')
        if not start_date:
            raise Exception('start date can not be None')
        response = HttpResponse(content_type='text/csv')
        name = f"cpchain-export-address-{address}"
        response['Content-Disposition'] = f'attachment; filename="{name}.csv"'

        writer = csv.writer(response)
        writer.writerow(['TxHash', 'Block', 'Timestamp', 'From', 'To', 'Value', 'TxFee'])

        # query filters
        filters = parse_txs_filter(request)
        # txs
        all_txs = txs_collection.find(
            filters, projection={'_id': False}).sort('_id', DESCENDING)
        
        for tx in all_txs:
            tx['value'] = currency.from_wei(tx['value'], 'ether')
            ts = dt.strftime(dt.fromtimestamp(tx['timestamp']), '%Y-%m-%d %H:%M:%S')
            writer.writerow([tx['hash'], tx['blockNumber'], ts, tx['from'], tx['to'], tx['value'], tx['txfee']])
        
        return response


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
                tx['contract'] = contract_collection.find(
                    {'txhash': tx['hash']})[0]['address']
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
            tx['contract'] = contract_collection.find(
                {'txhash': tx['hash']})[0]['address']
        tx['value'] = currency.from_wei(tx['value'], 'ether')
    return render(req, 'explorer/txs_list.html', {'txs': txs,
                                                  'blockNumber': block,
                                                  'txs_count': txs_count
                                                  })


def tx(req, tx_hash):
    # tx from hash
    search = tx_hash.strip().lower()

    tx_dict = list(txs_collection.find({"hash": search}))[0]
    tx_dict['gasLimit'] = block_collection.find(
        {'number': tx_dict['blockNumber']})[0]['gasLimit']
    tx_dict['gasPrice'] = format(tx_dict['gasPrice'] / 1e18, '.20f')
    tx_dict['txfee'] = format(tx_dict['txfee'], '.20f')
    tx_dict['value'] = currency.from_wei(tx_dict['value'], 'ether')
    try:
        input_data = cf.toText(hexstr=tx_dict['input'])
        input_data = input_data.replace('\\', r'\\')
        input_data = input_data.replace('`', r'\`')
    except Exception as e:
        input_data = tx_dict['input']

    if not tx_dict['to']:
        contract = contract_collection.find({'txhash': tx_hash})[0]['address']
        return render(req, 'explorer/tx_info.html', {'tx_dict': tx_dict, 'contract': contract, 'input': input_data})
    return render(req, 'explorer/tx_info.html', {'tx_dict': tx_dict, 'input': input_data})


class AddressView(viewsets.ViewSet):

    def retrieve(self, request, pk):
        """ 根据地址获取信息
        """
        address = pk
        raw_address = address
        try:
            raw_address = cf.toChecksumAddress(address.strip())
            address = raw_address.lower()
            code = contract_collection.find(
                {'address': raw_address})[0]['code']
            # code = cf.toHex(code)
        except Exception as e:
            code = '0x'
        try:
            txs_count = address_collection.find(
                {'address': address})[0]['txs_count']
        except:
            txs_count = 0

        balance = 'N/A'
        is_rnode = False
        try:
            if not NO_CHAIN_NODE:
                balance = currency.from_wei(
                    cf.cpc.getBalance(raw_address), 'ether')
                # check if the address have locked 200k cpc in RNode contract
                if rnode_collection.find({"Address": address}).count() > 0:
                    balance += 200000
                    is_rnode = True
        except Exception as e:
            print('cf connection error', e)
            balance = 'N/A'

        if code == '0x':
            proposer_history = block_collection.count(
                {'miner': address})
            return Response({
                'address': raw_address,
                'balance': balance,
                'txs_count': txs_count,
                'is_rnode': is_rnode,
                'proposer_history': proposer_history
            })
        else:
            creator = contract_collection.find(
                {'address': raw_address})[0]['creator']
            return Response({
                'address': raw_address,
                'balance': balance,
                'txs_count': txs_count,
                'code': code,
                'creator': creator,
            })


def address(req, address):
    raw_address = address
    try:
        raw_address = cf.toChecksumAddress(address.strip())
        address = raw_address.lower()
        code = contract_collection.find({'address': raw_address})[0]['code']
        # code = cf.toHex(code)
    except Exception as e:
        code = '0x'
    try:
        txs_count = address_collection.find(
            {'address': address})[0]['txs_count']
    except:
        txs_count = 0
    try:
        page = req.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    txs = txs_collection.find({'$or': [{'from': address}, {'to': address}]}).sort(
        'timestamp', DESCENDING)
    p = Paginator(txs, 25, request=req, fix_count=txs_count, restrain=True)
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
            d['contract'] = contract_collection.find(
                {'txhash': d['hash']})[0]['address']
        d['value'] = currency.from_wei(d['value'], 'ether')
        d['timesince'] = timenow - d['timestamp']

    # txs.sort(key=lambda x: x['timestamp'], reverse=True)

    balance = 'N/A'
    is_rnode = False
    try:
        if not NO_CHAIN_NODE:
            balance = currency.from_wei(
                cf.cpc.getBalance(raw_address), 'ether')
            # check if the address have locked 200k cpc in RNode contract
            if rnode_collection.find({"Address": address}).count() > 0:
                balance += 200000
                is_rnode = True
    except Exception as e:
        print('cf connection error', e)
        balance = 'N/A'

    # latest 25 txs
    current = {'begin': (int(page) - 1) * 25 + 1,
               'end': (int(page) - 1) * 25 + len(txs.object_list)}
    # current =1
    if code == '0x':
        proposer_history = block_collection.count(
            {'miner': address})
        return render(req, 'explorer/address.html', {'txs': txs, 'current': current,
                                                     'address': raw_address,
                                                     'balance': balance,
                                                     'txs_count': txs_count,
                                                     'is_rnode': is_rnode,
                                                     'proposer_history': proposer_history
                                                     })
    else:
        creator = contract_collection.find(
            {'address': raw_address})[0]['creator']
        return render(req, 'explorer/contract.html', {'txs': txs, 'current': current,
                                                      'address': raw_address,
                                                      'balance': balance,
                                                      'txs_count': txs_count,
                                                      'code': code,
                                                      'creator': creator,
                                                      })


class RNodesView(viewsets.ViewSet):

    def list(self, request):
        rnodes = list(rnode_collection.find(
            {'Address': {'$exists': True}}, projection={'_id': False}))
        proposerlist = list(proposer_collection.find())
        term = []
        if len(proposerlist) > 0:
            term = proposerlist[0].get('Term', [])
        try:
            rnodes.sort(key=lambda d: d['Rpt'], reverse=True)
        except Exception as e:
            log.error(e)
        return Response({
            'term': term,
            'rnodes': rnodes
        })


def rnode(req):
    rnodes = list(rnode_collection.find(({'Address': {'$exists': True}})))
    proposerlist = list(proposer_collection.find())
    if len(proposerlist) == 0:
        term = []
    else:
        term = proposerlist[0].get('Term', [])
    try:
        rnodes.sort(key=lambda d: d['Rpt'], reverse=True)
    except Exception:
        pass
    return render(req, 'explorer/rnode.html', {'term': term,
                                               'rnodes': rnodes})


class ProposersView(viewsets.ViewSet):

    def list(self, request):
        proposerlist = list(proposer_collection.find())[0]
        term = proposerlist.get('Term', [])
        view = int(proposerlist.get('View', 0))
        index = int(proposerlist.get('ProposerIndex', 0))
        termLen = proposerlist['TermLen'] if proposerlist else 1
        blockNumber = proposerlist['BlockNumber'] if proposerlist else 1
        proposers = proposerlist.get('Proposers', [])
        return Response({
            'term': term,
            'view': view,
            'index': index,
            'termLen': termLen,
            'blockNumber': blockNumber,
            'proposers': proposers
        })


def proposers(req):
    proposerlist = list(proposer_collection.find())[0]
    term = proposerlist.get('Term', [])
    view = int(proposerlist.get('View', 0))
    index = int(proposerlist.get('ProposerIndex', 0))
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
    events = list(event_collection.find(
        {'contract_address': address}, {'_id': 0, 'contract_address': 0}))
    queryset = abi_collection.find({'contract_address': address}, {
                                   '_id': 0, 'contract_address': 0})
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
        values = eth_abi.decode_abi(
            event['arg_types'], cf.toBytes(hexstr=data))
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
        queryset = abi_collection.find({'contract_address': address}, {
                                       '_id': 0, 'contract_address': 0})
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
        queryset = source_collection.find({'contract_address': address}, {
                                          '_id': 0, 'contract_address': 0})
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
    impeach_bks = block_collection.find({'impeachProposer': address}, {
                                        '_id': 0}).sort('number', DESCENDING)
    res = {}
    res['impeach_num'] = impeach_bks.count()
    res['success_num'] = block_collection.find({'miner': address}).count()
    res['impeach_bks'] = list(impeach_bks)
    return JsonResponse(res, safe=False)


def impeachs_by_block(req, block, isOur):
    block = int(block)
    impeach_bks = None
    if isOur == '0':
        impeach_bks = block_collection.find(
            {'number': {'$gt': block}, 'impeachProposer': {'$exists': True}},
            {'_id': False})
    elif isOur == '1':
        impeach_bks = block_collection.find(
            {'number': {'$gt': block}, 'impeachProposer': {'$exists': True},
             'impeachProposer': {'$in': our_proposer}},
            {'_id': False})
    res = {}
    res['impeach_num'] = impeach_bks.count()
    res['impeach_bks'] = list(impeach_bks)
    return JsonResponse(res)


def all_blocks(req):
    height = block_collection.find().sort(
        'number', DESCENDING).limit(1)[0]['number']
    height = int(height)
    blocks = block_collection.find({'number': {'$gt': (height - 1000)}},
                                   {'_id': False, 'transactions': False}).sort('number', DESCENDING)
    res = {}
    res['latest_1000_blocks'] = list(blocks)
    return JsonResponse(res)


def check_campaign(req):
    config = withdraw_abi.config
    campaign = cf.cpc.contract(
        abi=config["abi"], address="0x20BF49A0773a2b9eA5cF218C188d7F633b07c267")

    term = campaign.functions.termIdx().call()
    ten_candidates = []
    min = term - 10 if term - 10 >= 0 else 0
    for i in range(min, term):
        candidates = campaign.functions.candidatesOf(i).call()
        # for c in candidates:
        #     print(campaign.functions.candidateInfoOf(c).call())
        candidates = [c.lower() + ' *' if c.lower()
                      in our_proposer else c.lower() for c in candidates]

        ten_candidates.append({'term': i, 'candidates': candidates})
    ten_candidates = ten_candidates[::-1]

    return render(req, 'explorer/campaign.html', locals())


def candidate_info(req, addr):
    config = withdraw_abi.config
    campaign = cf.cpc.contract(
        abi=config["abi"], address="0xb8A07aE42E2902C41336A301C22b6e849eDd4F8B")
    if addr.endswith(' *'):
        addr = addr[:-2]

    addr = cf.toChecksumAddress(addr)
    info = campaign.functions.candidateInfoOf(addr).call()
    return JsonResponse(info, safe=False)


def impeachQuery(req):
    block = int(req.GET.get('block'))
    impeach_bks = block_collection.find(
        {'number': {'$gt': block}, 'impeachProposer': {'$exists': True}},
        {'_id': False})
    res = {}
    res['impeach_num'] = impeach_bks.count()
    res['impeach_bks'] = list(impeach_bks)
    bks = res.get('impeach_bks')
    li = []
    addr = {}
    for i in range(len(bks)):
        time = dt.fromtimestamp(
            bks[i]["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        impeach_item = {"address": bks[i]['impeachProposer'], 'number': bks[i]['number'],
                        'time': time}
        if impeach_item['address'] not in addr:
            addr[impeach_item['address']] = 1
        else:
            addr[impeach_item['address']] += 1
        li.append(impeach_item)
    # li.reverse()
    # sort them by number
    count_num = sorted(addr.items(), key=lambda x: x[1], reverse=True)
    return JsonResponse({"impeach_number": len(li), "impeach": count_num})


def impeachFrequency301(req):
    return redirect('explorer:impeachFrequency', days=7)


def impeachFrequency(req, days=7):
    now = int(time.time())
    day_zero = now - now % DAY_SECENDS
    chart = []
    for i in range(int(days)):
        gt_time = day_zero - (i + 1) * DAY_SECENDS
        lt_time = day_zero - i * DAY_SECENDS
        our_impeachs = block_collection.find(
            {'timestamp': {'$gte': gt_time, '$lt': lt_time}, 'impeachProposer': {'$exists': True},
             'impeachProposer': {'$in': our_proposer}}, {'_id': False}).count()
        all_impeachs = block_collection.find(
            {'timestamp': {'$gte': gt_time, '$lt': lt_time}, 'impeachProposer': {'$exists': True}}).count()
        com_impeachs = all_impeachs - our_impeachs
        our_success = block_collection.find(
            {'timestamp': {'$gte': gt_time, '$lt': lt_time}, 'impeachProposer': {'$exists': False},
             'miner': {'$in': our_proposer}}).count()
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
         'impeachProposer': {'$in': our_proposer}}, {'_id': False}).count()
    all_impeachs = block_collection.find(
        {'timestamp': {'$gte': day_zero}, 'impeachProposer': {'$exists': True}}).count()
    com_impeachs = all_impeachs - our_impeachs
    our_success = block_collection.find(
        {'timestamp': {'$gte': day_zero}, 'impeachProposer': {'$exists': False},
         'miner': {'$in': our_proposer}}).count()
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
        'our_icmpeach_frequency': our_impeach_frequency,
        'com_impeach_frequency': com_impeach_frequency,
        'date': 'today'
    })
    return render(req, 'explorer/impeachs.html', {'chart': chart})


class ProposerHistoryView(viewsets.ViewSet):
    filter_backends = [PageableBackend, ]

    def retrieve(self, request, pk):
        """ 获取 proposer 的出块历史
        """
        address = pk.lower()
        blocks_by_proposer = block_collection.find(
            {'miner': address}, projection={'_id': False, 'dpor': False}).sort('_id', DESCENDING)
        blocks_count = blocks_by_proposer.count()
        limit = int(request.GET.get('limit', 25))
        page = int(request.GET.get('page', 1))
        p = Paginator(blocks_by_proposer, limit,
                      request=request, fix_count=blocks_count)
        blocks = p.page(page)
        blocks.object_list = list(blocks.object_list)
        for b in blocks.object_list:
            b['txs_cnt'] = len(b['transactions'])
            del b['transactions']
        return Response({'results': blocks.object_list, 'page': page, 'address': address, 'count': blocks_count})


def proposer_history(req, address):
    address = address.lower()
    blocks_by_proposer = block_collection.find(
        {'miner': address}).sort('_id', DESCENDING)
    blocks_count = blocks_by_proposer.count()

    try:
        page = req.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(blocks_by_proposer, 25, request=req, fix_count=blocks_count)
    blocks = p.page(page)
    blocks.object_list = list(blocks.object_list)
    current = {'begin': (int(page) - 1) * 25 + 1,
               'end': (int(page) - 1) * 25 + len(blocks.object_list)}
    return render(req, 'explorer/proposer_history_list.html',
                  {'blocks': blocks, 'current': current, 'address': address, 'blocks_count': blocks_count})


# class AddressMarkViewSet(viewsets.ModelViewSet):
#     queryset = AddressMark.objects.filter()
#     serializer_class = AddressMarkSerializer
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated,)


# class AddressMarkTypeViewSet(viewsets.ModelViewSet):
#     queryset = AddressMarkType.objects.filter()
#     serializer_class = AddressMarkTypeSerializer
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated,)
