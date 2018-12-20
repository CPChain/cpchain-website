from cpchain_test.celery import app
from .faucet import Faucet

@app.task
def faucet(address):
    print("faucet start....")
    Faucet.send(address)
    Faucet.update(address)
    print("faucet finished....")