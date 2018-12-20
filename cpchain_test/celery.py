from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cpchain_test.settings')

app = Celery("faucet")
app.conf.update(
    BROKER_URL='amqp://localhost',
)
app.autodiscover_tasks(settings.INSTALLED_APPS)
