import time
from cpc_fusion import Web3
from cpc_fusion.middleware import geth_poa_middleware
from pymongo import DESCENDING, MongoClient

from cpchain_test.config import cfg

REFRESH_INTERVAL = 3

# chain

chain = 'http://{0}:{1}'.format(cfg['chain']['ip'], cfg['chain']['port'])
cf = Web3(Web3.HTTPProvider(chain))
cf.middleware_stack.inject(geth_poa_middleware, layer=0)

# mongodb
mongoHost = cfg['db']['ip']
client = MongoClient(host=mongoHost, port=27017)
rnode_collection = client['cpchain']['rnode']
proposer_collection = client['cpchain']['proposer']


def save_rnode_proposer():
    while True:
        rnodes = cf.cpc.getRNodes
        if rnodes:
            rnode_collection.remove({})
            rnode_collection.insert_many(rnodes)

        proposer = cf.cpc.getBlockGenerationInfo
        if proposer:
            proposer_collection.remove({})
            proposer_collection.insert_many(proposer)

        currentTerm = cf.cpc.getCurrentTerm
        if currentTerm:
            rnode_collection.update({'term':{'$exists':True}}, {'term': currentTerm}, True)

        currentView = cf.cpc.getCurrentView
        if currentView:
            rnode_collection.update({'view':{'$exists':True}}, {'view': currentView}, True)

        time.sleep(REFRESH_INTERVAL)


def main():
    while True:
        try:
            save_rnode_proposer()
        except Exception as e:
            print('rnode timeout>>>',e)
        time.sleep(10)


if __name__ == '__main__':
    print('start')
    main()