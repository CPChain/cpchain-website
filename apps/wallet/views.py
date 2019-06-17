from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.core import serializers


# Create your views here.

def community_detail(req, pk):
    data = serializers.serialize("json", WalletNews.objects.filter(pk=pk))
    return JsonResponse(data, safe=False)


# return msg:
# "[{\"model\": \"wallet.walletnews\", \"pk\": 2, \"fields\": {\"category\": \"News\", \"title\": \"321\", \"banner\": \"\", \"update_time\": \"2019-06-17\", \"content\": \"<p>fff</p>\"}}]"

def news_list(req):
    data = serializers.serialize("json", WalletNews.objects.all())
    return JsonResponse(data, safe=False)
