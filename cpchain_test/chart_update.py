import time

from pymongo import MongoClient
import sys

print(sys.argv)
from config import cfg
import json

DAY_SECENDS = 60 * 60 * 24
mongo = cfg['db']['ip']
port = int(cfg['db']['port'])
CLIENT = MongoClient(host=mongo, port=port, maxPoolSize=200)
txs_collection = CLIENT['cpchain']['txs']
address_collection = CLIENT['cpchain']['address']
chart_collection = CLIENT['cpchain']['chart']


def get_chart():
    ## chart
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
        add_day = address_collection.find({'timestamp': {'$lt': lt_time}}).count()
        chart.append({'time': dt, 'tx': txs_day, 'bk': add_day})
    chart.reverse()
    chart = json.dumps(chart)
    chart_collection.update({}, {'chart': chart}, upsert=True)


get_chart()
