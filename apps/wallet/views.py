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

def news_list(req):
    news_list = WalletNews.objects.all()
    data = serializers.serialize("json",news_list,
                                 fields=('pk', 'category', 'title', 'banner', 'update_time'))
    return JsonResponse(data, safe=False)
