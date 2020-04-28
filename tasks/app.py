from celery import Celery

from tasks.sync_congress import sync_congress
from tasks.sync_proposals import sync_proposals
from tasks.check_timeout import check_timeout
from tasks.chart_update import update_chart
from tasks.send_email import send_email

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
def check_timeout_task():
    log = get_log('celery')
    log.info('check timeout task')
    check_timeout()

@app.task
def chart_update_task():
    log = get_log('celery')
    log.info('update chart task')
    update_chart()

@app.task
def auto_send_email():
    log = get_log('send-email')
    log.info('send email')
    send_email()

@app.task
def rnode_update():
    pass

@app.task
def rate_update():
    pass
