from celery import Celery

from sync_congress import sync_congress
from sync_proposals import sync_proposals

from log import get_log

log = get_log('celery')

app = Celery()
app.config_from_object('tasks.config')

log.info("start celery worker/beat")

@app.task
def sync_congress_task():
    # sync the data of congress contract from chain
    log = get_log('celery')
    log.info('sync congress task')
    sync_congress()

@app.task
def sync_proposals_task():
    log = get_log('celery')
    log.info('sync proposals task')
    sync_proposals()

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
