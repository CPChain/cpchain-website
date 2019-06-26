import time

from cpc_fusion import Web3
from pymongo import MongoClient

from cpchain_test.config import cfg

REFRESH_INTERVAL = 3

# chain

chain = 'http://{0}:{1}'.format(cfg['chain']['ip'], cfg['chain']['port'])
cf = Web3(Web3.HTTPProvider(chain))

# mongodb
mongoHost = cfg['mongo']['ip']
port = int(cfg['mongo']['port'])

client = MongoClient(host=mongoHost, port=port)
uname = cfg['mongo']['uname']
pwd = cfg['mongo']['password']
db = client['cpchain']
db.authenticate(uname, pwd)
rnode_collection = client['cpchain']['rnode']
proposer_collection = client['cpchain']['proposer']
proposer_history_collection = client['cpchain']['proposer_history']

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
            proposer_history_collection.update_one({"Term":proposer.get('Term')}, {"$set": proposer}, upsert=True)
            
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
