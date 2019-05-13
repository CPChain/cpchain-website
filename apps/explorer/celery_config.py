# encoding: utf-8
# Author: Timeashore
from datetime import timedelta
from celery.schedules import crontab

# celery
BROKER_URL = 'redis://localhost:6379/0'                 # 使用Redis作为消息代理
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'      # 把任务结果存在了Redis

CELERY_TIMEZONE='Asia/Shanghai'                         # 指定时区，默认是 UTC

CELERY_TASK_SERIALIZER = 'pickle'                       # 任务序列化和反序列化使用pickle方案
CELERY_RESULT_SERIALIZER = 'json'                       # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24               # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
CELERY_ACCEPT_CONTENT = ['json','pickle']               # 指定接受的内容类型

CELERY_IMPORTS = (                                  # 指定导入的任务模块
    'apps.explorer.tasks',
)
CELERYBEAT_SCHEDULE = {
    # 'add-every-10-seconds': {
    #      'task': 'chat.tasks.add',
    #      'schedule': timedelta(seconds=10),          # 每 30 秒一次
    #      # 'schedule': timedelta(minutes=1),         # 每 1 分钟一次
    #      # 'schedule': timedelta(hours=4),           # 每 4 小时一次
    #      'args': (5, 8)                              # 任务函数参数
    # },
    # 'multiply-at-some-time': {
    #     'task': 'chat.tasks.multiply',
    #     'schedule': crontab(hour=9, minute=50),      # 每天早上 9 点 50 分执行一次
    #     'args': (3, 7)                               # 任务函数参数
    # },
    'updateInfo-every-3-seconds': {
        'task': 'apps.explorer.tasks.updateInfo',
        'schedule': timedelta(seconds=3),          # 每 3 秒一次
        # 'args': ()                               # 任务函数参数
    }
}