"""

redis

"""

from cpchain_test.settings import REDIS_CONFIG, CACHE_CONFIG

import redis
import json

ROOT = "cpchain-website$"
TX_CHANNEL = ROOT + "tx$"

# connect pool
conn_pool = redis.ConnectionPool(
    host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'])


def get_redis_client():
    return redis.Redis(connection_pool=conn_pool)


def push_tx(rc: redis.Redis, frm: str, tx: str):
    max_cnt = CACHE_CONFIG['MAX_TX_COUNT_PER_ADDR']
    channel = TX_CHANNEL + frm
    if rc.llen(channel) >= max_cnt:
        rc.rpop(channel)
    rc.lpush(channel, tx)


def count_tx(rc: redis.Redis, frm: str):
    """ 获取 frm 地址的交易数量
    """
    channel = TX_CHANNEL + frm
    return rc.llen(channel)


def tail_tx(rc: redis.Redis, frm: str):
    """ 获取最后一笔交易
    """
    channel = TX_CHANNEL + frm
    if rc.llen(channel) < 0:
        return None
    return rc.lindex(channel, 0)


def query_tx(rc: redis.Redis, frm: str, limit: int, offset: int):
    start = offset
    channel = TX_CHANNEL + frm
    end = max(start+limit, rc.llen(channel)-1)
    return [json.loads(i) for i in rc.lrange(channel, start, end)]


def clean_tx(rc: redis.Redis, frm: str):
    """ 删除缓存
    """
    rc.delete(TX_CHANNEL + frm)
