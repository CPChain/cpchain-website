"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
import threading
import time
import json
import signal
import sys

from channels.routing import get_default_application
from asgiref.sync import async_to_sync

import log

log = log.get_log('daphne')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cpchain_test.settings")
django.setup()

# start an async thread to push blocks

def run(run_event):
    while run_event.is_set():
        try:
            from channels.layers import get_channel_layer
            from apps.explorer.views import wshandler
            channel_layer = get_channel_layer()
            data = wshandler()
            channel_name = 'ws_explorer'
            async_to_sync(channel_layer.group_send)(channel_name, {
                'type': 'update_message',
                'message': json.dumps(data),
            })
            log.info('push block: ' + str(data['header']['blockHeight']))
            time.sleep(3)
        except Exception as e:
            time.sleep(10)
            print(e)

run_event = threading.Event()
run_event.set()

t = threading.Thread(target=run, args=(run_event,))
t.start()

def signal_handler(sig, frame):
    log.info('stop daphne by ctrl+c')
    run_event.clear()
    t.join()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

application = get_default_application()
