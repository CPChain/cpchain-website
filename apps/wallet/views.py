from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.core import serializers
import json


# Create your views here.

def community_detail(req, pk):
    data = serializers.serialize("json", WalletNew.objects.filter(pk=pk))
    return JsonResponse(data, safe=False)


# return msg:
# "[{\"model\": \"wallet.WalletNew\", \"pk\": 2, \"fields\": {\"category\": \"News\", \"title\": \"321\", \"banner\": \"\", \"update_time\": \"2019-06-17\", \"content\": \"<p>fff</p>\"}}]"

def news_list(req, lang):
    if lang == 'en':
        news_list = WalletNew.objects.filter(category='News_en')
    elif lang == 'cn':
        news_list = WalletNew.objects.filter(category='News_cn')

    data = serializers.serialize("json", news_list,
                                 fields=('pk', 'category', 'title', 'banner', 'update_time'))
    return JsonResponse(data, safe=False)


def evnet_list(req, lang):
    if lang == 'en':
        evnet_list = WalletEvent.objects.filter(category='Event_en')
    elif lang == 'cn':
        evnet_list = WalletEvent.objects.filter(category='Event_cn')

    data = serializers.serialize("json", evnet_list,
                                 fields=('pk', 'category', 'title', 'banner', 'update_time'))
    return JsonResponse(data, safe=False)
