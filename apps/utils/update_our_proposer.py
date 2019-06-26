import os
import sys

from pymongo import MongoClient

sys.path.append('../..')
os.chdir(sys.path[0])
from cpchain_test.config import cfg

# mongodb
mongoHost = cfg['db']['ip']
port = int(cfg['db']['port'])

CLIENT = MongoClient(host=mongoHost, port=port)
uname = cfg['db']['uname']
pwd = cfg['db']['password']
db = CLIENT['cpchain']
db.authenticate(uname, pwd)

our_proposer = CLIENT['cpchain']['our_proposer']

ours = ['0x27c3500c8a493a152f1dfdec162c422b3678b03e',
        '0xf285996f36aa76adf637c60f2005da637efd71aa',
        '0x50bf9d407d8e30b8124f3711df97611d76d45699',
        '0x99fc3138ff48a4fae3a0e65c6f83266a5284a683',
        '0xf6f59e901b3cd551f1753dfe80ab806bb0046b30',
        '0xa3a0fe044eb8ce1731ed99ca0901a795abf58da8',
        '0x45f40e0c7135d86d92a88443a160045a2897436e',
        '0x0005efc08c5ff71c3538ebc85b1bb93c377cef14',
        '0x46ac4607b5334b5dc7cd671b0c11c5ffa81324f6',
        '0x1573ce2ab9a0113d25ce5e7a74b564a02f9058ad',
        '0x01cf3229840fc212d54df720cdae3e6d04320a9c',
        '0xaa8ad61eb978bbde0b6f69d2cd3033755d8f9d04', ]


def update_proposer():
    our_proposer.update({}, {'our_proposer': ours})


def read_our_proposer():
    p = list(our_proposer.find({}, {'_id': 0}))
    if len(p) == 0:
        ours = []
    else:
        ours = p[0].get('our_proposer')

    return ours

if __name__ == '__main__':
    update_proposer()