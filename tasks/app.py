from celery import Celery

from functools import reduce
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from tasks.sync_congress import sync_congress
from tasks.sync_proposals import sync_proposals
from tasks.check_timeout import check_timeout
from tasks.chart_update import update_chart
from tasks.send_email import send_email

from log import get_log

import time
import requests
import json
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'cpchain_test.settings'
channel_layer = get_channel_layer()

from apps.explorer.views import wshandler
from node_ip.models import IP

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
def pushBlocksInfo():
    data = wshandler()
    async_to_sync(channel_layer.group_send)('ws_explorer', {
        'type': 'update_message',
        'message': json.dumps(data),
    })
    return data['header']

@app.task
def rnode_update():
    pass

@app.task
def rate_update():
    pass


def ip_into_int(ip):
    # 先把 192.168.31.46 用map分割'.'成数组，然后用reduuce+lambda转成10进制的 3232243502
    # (((((192 * 256) + 168) * 256) + 31) * 256) + 46
    return reduce(lambda x, y:(x<<8)+y, map(int,ip.split('.')))
 
# 掩码对比判断 IP 是否为内网 IP
def is_internal_ip(ip_str):
    ip_int = ip_into_int(ip_str)
    net_A = ip_into_int('10.255.255.255') >> 24
    net_B = ip_into_int('172.31.255.255') >> 20
    net_C = ip_into_int('192.168.255.255') >> 16
    net_ISP = ip_into_int('100.127.255.255') >> 22
    net_DHCP = ip_into_int('169.254.255.255') >> 16
    return ip_int >> 24 == net_A or ip_int >>20 == net_B or ip_int >> 16 == net_C or ip_int >> 22 == net_ISP or ip_int >> 16 == net_DHCP

@app.task
def get_geo_for_ip():
    qs = IP.objects.filter(deleted=False, handled=False)
    log = get_log('geo-ip')
    for obj in qs:
        try:
            ip = obj.ip
            if ip not in ['127.0.0.1', 'localhost'] and not is_internal_ip(ip):
                log.info("handle: " + ip)
                resp = requests.get(url = 'http://ip-api.com/json/%s' % (ip))
                data = resp.json()
                if data['status'] != 'fail':
                    obj.longitude = data['lon']
                    obj.latitude = data['lat']
                    obj.country = data['country']
                    obj.city = data['city']
                    obj.isp = data['isp']
                    obj.countryCode = data['countryCode']
                    obj.region = data['region']
                    obj.regionName = data['regionName']
                else:
                    log.info(ip + " is in private net reported by ip-api")
                time.sleep(3)
            else:
                log.info(ip + " is in private net")
            obj.handled = True
            obj.save()
        except Exception as e:
            log.error(e)
