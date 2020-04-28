import sys
import time

from pymongo import MongoClient

from cpchain_test.config import cfg
import json

DAY_SECENDS = 60 * 60 * 24
mongo = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])


def update_chart():
    CLIENT = MongoClient(host=mongo, port=port, maxPoolSize=200)
    uname = cfg['mongo']['uname']
    pwd = cfg['mongo']['password']
    db = CLIENT['cpchain']
    db.authenticate(uname, pwd)
    txs_collection = CLIENT['cpchain']['txs']
    address_collection = CLIENT['cpchain']['address']
    chart_collection = CLIENT['cpchain']['chart']
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

if __name__ == '__main__':

    update_chart()
