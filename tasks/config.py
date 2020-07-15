# encoding: utf-8

import os, sys
from datetime import timedelta

from cpchain_test.config import cfg

CELERY_REDIS_HOST = cfg['redis']['host']
CELERY_REDIS_PORT = cfg['redis']['port']

# celere
BROKER_URL = f'redis://{CELERY_REDIS_HOST}:{CELERY_REDIS_PORT}/0'  # 使用Redis作为消息代理
CELERY_RESULT_BACKEND = f'redis://{CELERY_REDIS_HOST}:{CELERY_REDIS_PORT}/0'  # 把任务结果存在了Redis


CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

CELERY_IMPORTS = (  # 指定导入的任务模块
    # 'apps.explorer.tasks',
    'tasks.app'
)

CELERYBEAT_SCHEDULE = {
    # 'updateInfo-every-3-seconds': {
    #     'task': 'apps.explorer.tasks.updateInfo',
    #     'schedule': timedelta(seconds=3),  # 每 3 秒一次
    # },
    'sync-congress': {
        'task': 'tasks.app.sync_congress_task',
        'schedule': timedelta(seconds=10),
    },
    'sync-proposals': {
        'task': 'tasks.app.sync_proposals_task',
        'schedule': timedelta(seconds=10),
    },
    'check-timeout': {
        'task': 'tasks.app.check_timeout_task',
        'schedule': timedelta(hours=1),
    },
    'update-chart': {
        'task': 'tasks.app.chart_update_task',
        'schedule': timedelta(hours=1),
    },
    'auto-send-email': {
        'task': 'tasks.app.auto_send_email',
        'schedule': timedelta(minutes=1),
    },
    'updateInfo-every-3-seconds': {
        'task': 'tasks.app.pushBlocksInfo',
        'schedule': timedelta(seconds=3),
    },
    'geo-ip': {
        'task': 'tasks.app.get_geo_for_ip',
        'schedule': timedelta(seconds=30)
    }
}
