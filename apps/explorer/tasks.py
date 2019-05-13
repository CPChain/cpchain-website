import json

from apps.explorer import cele
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import os


os.environ['DJANGO_SETTINGS_MODULE'] = 'cpchain_test.settings'
channel_layer = get_channel_layer()


def send_channel_msg(channel_name,data):
    async_to_sync(channel_layer.group_send)(channel_name, {
        'type': 'update_message',
        'message': json.dumps(data),
    })

from .views import wshandler
@cele.task
def updateInfo():
    data =wshandler()
    send_channel_msg('ws_explorer',data)
    return data['header']