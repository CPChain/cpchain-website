"""

缓存数据

sudo docker run -d --name sync-for-cache -v `pwd`:/cpchain-website liaojl/website python sync_for_cache.py

sudo docker logs -f --since 1m sync-for-cache

"""

import time
import json

from log import get_log
from tools.dingding import post_message
from apps.chain.db import txs_collection

from tools import redis_helper as rh

logger = get_log('sync-for-cache')

def sync_for_cache(txs):
    try:
        rc = rh.get_redis_client()
        current_tx_ts = 0
        while True:
            filters = {
                "value": {
                    "$gt": 0
                },
                "timestamp": {
                    "$gte": current_tx_ts
                }
            }
            count = txs.count_documents(filters)
            logger.info("txs count: %d, current timestamp: %d", count, current_tx_ts)
            # 获取所有的 value 不为 0 的交易
            cursor = txs.find(filters, projection={"_id": False})
            for r in cursor:
                current_tx_ts = r['timestamp']
                # 获取此 from 的最后一笔交易，判断时间戳，只有之后的时间戳，可加入
                latest = rh.tail_tx(rc, r['from'])
                if latest != None:
                    tx = json.loads(latest)
                    if r['timestamp'] <= tx['timestamp']:
                        continue
                rh.push_tx(rc, r['from'], json.dumps(r))
            time.sleep(10)
    except Exception as e:
        logger.error(e)
        post_message(f"**sync for cache error:**\n{e}")

if __name__ == '__main__':
    sync_for_cache(txs_collection)

