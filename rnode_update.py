import time
from cpc_fusion import Web3
from pymongo import DESCENDING, MongoClient

from cpchain_test.config import cfg

REFRESH_INTERVAL = 3

# chain

chain = 'http://{0}:{1}'.format(cfg['chain']['ip'], cfg['chain']['port'])
cf = Web3(Web3.HTTPProvider(chain))

# mongodb
mongoHost = cfg['db']['ip']
client = MongoClient(host=mongoHost, port=27017)
rnode_collection = client['cpchain']['rnode']
proposer_collection = client['cpchain']['proposer']
proposer_history_collection = client['cpchain']['proposerhistory']

def save_rnode_proposer():
    while True:
        rnodes = cf.cpc.getRNodes
        if rnodes:
            rnode_collection.remove({})
            rnode_collection.insert_many(rnodes)

        proposer = cf.cpc.getBlockGenerationInfo
        if proposer:
            proposer = dict(proposer)
            proposer_collection.remove({})
            # if proposer['Proposer'].endswith('000000'):
            #     proposer['Proposer'] = cf.cpc.getProposerByBlock(proposer['BlockNumber'])
            proposer_collection.update_one({}, {"$set": proposer}, upsert=True)
            # proposer_history_collection.insert(proposer)
            proposer_history_collection.remove({})
            proposer_history_collection.update_one({}, {"$set": proposer}, upsert=True)

        currentTerm = cf.cpc.getCurrentTerm
        if currentTerm:
            rnode_collection.update({'term': {'$exists': True}},  {'term': currentTerm}, True)

        currentView = cf.cpc.getCurrentView
        if currentView:
            rnode_collection.update({'view': {'$exists': True}}, {'view': currentView + 1}, True)

        time.sleep(REFRESH_INTERVAL)


def main():
    while True:
        try:
            save_rnode_proposer()
        except Exception as e:
            print('rnode timeout>>>', e)
        time.sleep(10)


if __name__ == '__main__':
    print('start')
    main()
