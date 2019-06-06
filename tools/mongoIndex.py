from pymongo import  MongoClient
from cpchain_test.config import cfg

mongoHost = cfg['db']['ip']
client = MongoClient(host=mongoHost, port=27017)
b_collection = client['cpchain']['blocks']
tx_collection = client['cpchain']['txs']
address_collection = client['cpchain']['address']
contract_collection = client['cpchain']['contract']

def create_index():
    # block collection
    b_collection.ensure_index({'number':1})
    b_collection.ensure_index({'hash':1})
    # txs collection
    tx_collection.ensure_index({'blockNumber':1})
    tx_collection.ensure_index({'hash':1})
    tx_collection.ensure_index({'from':1})
    tx_collection.ensure_index({'to':1})
    tx_collection.ensure_index({'timestamp':-1})
    tx_collection.ensure_index({'from':1,'timestamp':-1})
    tx_collection.ensure_index({'to':1,'timestamp':-1})



if __name__ == '__main__':
    create_index()