"""

chain RESTful APIs

"""

from sys import flags
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from django_filters import compat

from cpchain_test.settings import cf
from log import get_log

from tools import redis_helper as rh

from .db import txs_collection, rnode_reward_total_col

log = get_log('app')


def check_flag(tx, address): return None if address is None else (
    'self' if tx['from'] == tx['to'] else ('in' if tx['to'] == address else 'out'))


def hanle_value(value): return '%.4f' % cf.fromWei(value, 'ether')


class PageableBackend(BaseFilterBackend):

    def filter_queryset(self, request, qs, view):
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='limit',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="每页大小"
                )
            ),
            compat.coreapi.Field(
                name='page',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="页码，从0开始"
                )
            ),
        ]


class TxFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, qs, view):
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='address',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="指定获取此钱包地址内的交易"
                )
            ),
            compat.coreapi.Field(
                name='flag',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="交易类型：in/out"
                )
            ),
            compat.coreapi.Field(
                name='exclude_empty_value',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="是否排除 value 为 0 的交易（仅 address 不为空时有效）, true/false，默认为 true"
                )
            ),
        ]


def handle_tx(tx, address):
    return {
        'value': float(hanle_value(tx['value'])),
        'time': tx['timestamp'],
        'txhash': tx['hash'],
        'from': tx['from'],
        'to': tx['to'],
        'flag': check_flag(tx, address),
        'txfee': tx['txfee'],
        'block': tx['blockNumber'],
        'status': tx['status'],
        'input': tx['input']
    }


class TxViewSet(viewsets.ViewSet):
    """
    获取交易记录
    """
    filter_backends = [TxFilterBackend, PageableBackend]

    def list(self, request):
        """ 交易记录列表

        + `flag`: 交易类型：in/out，只有 address 不为空时起作用
        + `address`: 指定获取此钱包地址内的交易
        + `limit`: 每页大小，默认为 20
        + `page`: 页码，从 0 开始，默认为 0
        + `exclude_empty_value`: 是否排除 value 为 0 的交易（仅 address 不为空时有效）, true/false，默认为 true
        """
        address = request.GET.get('address')
        flag = request.GET.get('flag')
        limit = request.GET.get('limit', 20)
        page = request.GET.get('page', 0)
        exclude_empty_value = request.GET.get('exclude_empty_value', 'true')

        exclude_empty_value = exclude_empty_value == 'true'
        try:
            limit = min(100, int(limit))
            if limit < 1:
                limit = 20
            page = int(page)
            if page < 0:
                page = 0
        except Exception as e:
            limit = 20
            page = 0
            log.error(e)

        count = 0
        txs = []
        if flag in ['in', 'out'] or not exclude_empty_value:
            # 从 mongodb 中获取
            filters = {}

            if address:
                address = cf.toChecksumAddress(address.strip()).lower()
                address_filter = {'$or': [{'from': address}, {'to': address}]}
                if flag == 'in':
                    address_filter = {'to': address}
                elif flag == 'out':
                    address_filter = {'from': address}                

                filters = address_filter
                if exclude_empty_value:
                    filters = {'$and': [
                        address_filter,
                        {'value': {'$ne': 0.0}}
                    ]}

            found = txs_collection.find(filters)
            count = found.count()
            txs = found.sort('timestamp', -1).limit(limit).skip(page * limit)
        elif address:
            # 从缓存中获取
            rc = rh.get_redis_client()
            count = rh.count_tx(rc, address)
            txs = rh.query_tx(rc, address, limit, page*limit)

        txs_wallet = []
        for tx in txs:
            _tx = {
                'value': float(hanle_value(tx['value'])),
                'time': tx['timestamp'],
                'txhash': tx['hash'],
                'from': tx['from'],
                'to': tx['to'],
                'flag': check_flag(tx, address),
                'txfee': tx['txfee'],
                'block': tx['blockNumber'],
                'status': tx['status'],
                'input': tx['input']
            }
            txs_wallet.append(_tx)
        results = {
            'results': txs_wallet,
            'count': count,
            'limit': limit,
            'page': page,
        }
        return Response(results)

    def retrieve(self, request, pk=None):
        """ 通过交易 hash 获取交易记录
        """
        address = request.GET.get('address')
        if pk is not None:
            found = txs_collection.find({'hash': pk})
            if found.count() == 0:
                return Response({
                    "code": 1,
                    "message": "The transaction not found"
                }, status=404)
            return Response(handle_tx(found[0], address))
        return Response({})


class RNodeRewardFilterBackend(BaseFilterBackend):
    """
    RNode rewards
    """

    def filter_queryset(self, request, qs, view):
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='address',
                required=True,
                location='query',
                schema=compat.coreschema.String(
                    description="指定获取此钱包地址内的交易"
                )
            ),
        ]


class RNodeRewardViewSet(viewsets.ViewSet):
    """
    RNode reward 查询
    """
    filter_backends = [RNodeRewardFilterBackend,]

    def list(self, request):
        """ RNode rewards 查询

        + `reward`: 总收益
        + `total_blocks`: 总出块数
        + `today_reward`: 今日收益
        + `today_blocks`: 今日出块数
        """
        addr = request.GET['address']
        result = {
            'reward': 0,
            'total_blocks': 0,
            'today_reward': 0,
            'today_blocks': 0,
        }
        addr = addr.lower()
        if rnode_reward_total_col.count_documents({'miner': addr}) == 0:
            return Response(result)
        result = rnode_reward_total_col.find({'miner': addr}, projection={"_id": False})[0]
        return Response(result)
