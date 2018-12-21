from pymongo import DESCENDING, MongoClient
from cpchain_test.config import cfg

mongo = cfg['db']['ip']
db = cfg['db']['db']
