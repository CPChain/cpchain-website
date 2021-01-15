import logging.handlers
from cpc_fusion import Web3
from cpchain_test.config import cfg

# chain config
chain = 'http://{0}:{1}'.format(cfg['chain']['ip'], cfg['chain']['port'])

# cpc fusion
cf = Web3(Web3.HTTPProvider(chain))
