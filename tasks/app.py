from celery import Celery

from sync_congress import sync_congress
from log import get_log

log = get_log('celery')

app = Celery()
app.config_from_object('tasks.config')

@app.task
def sync_congress_task():
    # sync the data of congress contract from chain
    log.info('sync congress task')
    sync_congress()

@app.task
def sync_proposal():
    pass

@app.task
def check_timeout():
    pass

@app.task
def chart_update():
    pass

@app.task
def send_email():
    pass

@app.task
def rnode_update():
    pass

@app.task
def rate_update():
    pass
