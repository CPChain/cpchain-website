from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.core import serializers
import json
from django.db.models import Q


# Create your views here.

def news_detail(req, pk):
    data = serializers.serialize("json", WalletNew.objects.filter(pk=pk))
    return JsonResponse(data, safe=False)


#    ('News_cn', 'News_cn'),
#     ('Event_en', 'Event_en'),
# ('Event_cn', 'Event_cn'),
def news_list(req, lang):
    if lang == 'en':
        news_list = list(WalletNew.objects.filter(category='News_en').values('pk', 'category', 'title', 'banner',
                                                                             'update_time'))
        events_list = list(WalletNew.objects.filter(category='Event_en').values('pk', 'category', 'title', 'banner',
                                                                                'update_time'))
    elif lang == 'cn':
        news_list = list(WalletNew.objects.filter(category='News_cn').values('pk', 'category', 'title', 'banner',
                                                                             'update_time'))
        events_list = list(WalletNew.objects.filter(category='Event_cn').values('pk', 'category', 'title', 'banner',
                                                                                'update_time'))

    msg = {'news': news_list, 'events': events_list}

    return JsonResponse(json.dumps(msg))


def swipe(req):
    pass
