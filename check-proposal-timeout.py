"""

check timeout

"""

from log import get_log
from cpc_fusion import Web3
from datetime import datetime as dt
from cpchain_test.config import cfg
import django
import logging
import os
import pytz
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cpchain_test.settings')
django.setup()

def load_key(key):
    with open(key, 'r') as fr:
        return fr.read()


def load_password(password):
    with open(password, 'r') as fr:
        return "".join(fr.readlines()).strip()


log = get_log('check-proposal-timeout')

host = cfg["chain"]["ip"]
port = cfg["chain"]["port"]
address = cfg['community']['proposal']

log.info(f"chain rpc interface: http://{host}:{port}")
log.info(f'congress constract\'s address is {address}')

cf = Web3(Web3.HTTPProvider(f'http://{host}:{port}'))

key = cfg['community']['keystore']
password = cfg['community']['password_path']
owner = cf.toChecksumAddress(cfg['community']['owner'])
chainID = int(cfg['community']['chainID'])

log.info("decrypt keys")
decrypted_key = cf.cpc.account.decrypt(load_key(key), load_password(password))


# ProposalABI is the input ABI used to generate the binding from.
abi = cfg['community']['proposalABI'][1:-1].replace('\\', '')
instance = cf.cpc.contract(abi=abi, address=address)


def main():
    cnt = instance.functions.getProposalsCnt().call()
    log.info(f"proposal's count is {cnt}")
    # iterate
    for i in range(cnt):
        try:
            proposal = instance.call().proposalsIDList(i)
            status = instance.functions.getStatus(proposal).call()
            if status != 2 and status != 3:
                gas_price = cf.cpc.gasPrice
                nonce = cf.cpc.getTransactionCount(owner)
                # estimate gas
                gas = instance.functions.checkTimeout(proposal).estimateGas()
                log.info(f"nonce: {nonce}, gasPrice: {gas_price}, gas: {gas}, chainID: {chainID}")
                tx = instance.functions.checkTimeout(proposal).buildTransaction(
                    {"gasPrice": gas_price, "nonce": nonce,  "gas": gas, "from": owner, "value": 0})
                tx['type'] = 0
                tx['chainId'] = chainID
                signed_txn = cf.cpc.account.signTransaction(tx, decrypted_key)
                log.info('signed tx')
                tx_hash = cf.cpc.sendRawTransaction(signed_txn.rawTransaction)
                log.info(f'sended tx')
                tx_receipt = cf.cpc.waitForTransactionReceipt(tx_hash)
                log.info(f'sccessfully update the status of {proposal} to timeout')
        except Exception as e:
            log.error(e)


if __name__ == '__main__':
    main()
