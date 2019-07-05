from celery import Celery

cele = Celery('celery_ws')
cele.config_from_object('apps.explorer.celery_config')
