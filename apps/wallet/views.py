from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.core import serializers
import json


# Create your views here.

def community_detail(req, pk):
    data = serializers.serialize("json", WalletNews.objects.filter(pk=pk))
    return JsonResponse(data, safe=False)


# return msg:
# "[{\"model\": \"wallet.walletnews\", \"pk\": 2, \"fields\": {\"category\": \"News\", \"title\": \"321\", \"banner\": \"\", \"update_time\": \"2019-06-17\", \"content\": \"<p>fff</p>\"}}]"

def news_list(req, lang):
    if lang == 'en':
        news_list = WalletNews.objects.filter(category='News_en')
    elif lang == 'cn':
        news_list = WalletNews.objects.filter(category='News_cn')

    data = serializers.serialize("json", news_list,
                                 fields=('pk', 'category', 'title', 'banner', 'update_time'))
    return JsonResponse(data, safe=False)
