"""

redis test

"""

import redis
import json

# 连接池连接使用，节省了每次连接用的时间
conn_pool = redis.ConnectionPool(host='localhost',port=6379)

rc = redis.Redis(connection_pool=conn_pool)

prefix = "test"

def main():
    data = [{'id': i, 'name': 'a'+str(i)} for i in range(10)]
    channel = prefix+"$"+"tx"
    for r in data:
        rc.lpush(channel, json.dumps(r))
    print(rc.llen(channel))
    item = rc.lrange(channel, 0, -1)[2]
    print(item)
    for i in range(rc.llen(channel)):
        rc.rpop(channel)
    print(rc.llen(channel))

if __name__ == '__main__':
    main()

