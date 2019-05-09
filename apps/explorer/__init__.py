from celery import Celery

cele = Celery('celery_ws')                                # 创建 Celery 实例
cele.config_from_object('apps.explorer.celery_config')