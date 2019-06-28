import os
import sys

from pymongo import MongoClient

sys.path.append('../..')
os.chdir(sys.path[0])
from cpchain_test.config import cfg

# mongodb
mongoHost = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])

CLIENT = MongoClient(host=mongoHost, port=port)
uname = cfg['mongo']['uname']
pwd = cfg['mongo']['password']
db = CLIENT['cpchain']
db.authenticate(uname, pwd)

our_proposer = CLIENT['cpchain']['our_proposer']

ours = ['0x50f8c76f6d8442c54905c74245ae163132b9f4ae',
        '0x8ab63651e6ce7eed40af33276011a5e2e1a533a2',
        '0x501f6cf7b2437671d770998e3b785474878fef1d',
        '0x9508e430ce672750bcf6bef9c4c0adf303b28c5c',
        '0x049295e2e925cec28ddeeb63507e654b6d317423',
        '0x8c65cb8568c4945d4b419af9066874178f19ba43',
        '0x4d1f1d14f303b746121564e3295e2957e74ea5d2',
        '0x73ae2b32ef3fad80707d4da0f49c675d3efc727c',
        '0x5a55d5ef67c047b5d748724f7401781ed0af65ed',
        '0x1f077085dfdfa4a65f8870e50348f277d6fcd97c',
        '0xcb6fb6a201d6c126f80053fe17ca45188e24fe2f',
        '0xfaf2a2cdc4da310b52ad7d8d86e8c1bd5d4c0bd0']


def update_proposer():
    our_proposer.drop()
    our_proposer.insert({'our_proposer': ours})


def read_our_proposer():
    p = list(our_proposer.find({}, {'_id': 0}))
    if len(p) == 0:
        ours = []
    else:
        ours = p[0].get('our_proposer')

    return ours


if __name__ == '__main__':
    update_proposer()
