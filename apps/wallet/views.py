from django.core import serializers
from django.http import JsonResponse

from .models import *


# Create your views here.

def news_detail(req, pk):
    data = serializers.serialize("json", WalletNew.objects.filter(pk=pk))
    return JsonResponse(data, safe=False)


#    ('News_cn', 'News_cn'),
#     ('Event_en', 'Event_en'),
# ('Event_cn', 'Event_cn'),
def events_list(req, lang):
    if lang == 'en':
        events_list = WalletNew.objects.filter(category='Event_en').values('pk', 'category', 'title', 'banner',
                                                                           'update_time')
    elif lang == 'cn':
        events_list = WalletNew.objects.filter(category='Event_cn').values('pk', 'category', 'title', 'banner',
                                                                           'update_time')

    msg = serializers.serialize('json', events_list)
    return JsonResponse(msg, safe=False)


def news_list(req, lang):
    if lang == 'en':
        news_list = WalletNew.objects.filter(category='News_en').values('pk', 'category', 'title', 'banner',
                                                                        'update_time')
    elif lang == 'cn':
        news_list = WalletNew.objects.filter(category='News_cn').values('pk', 'category', 'title', 'banner',
                                                                        'update_time')

    msg = serializers.serialize('json', news_list)
    return JsonResponse(msg, safe=False)


def swipe(req):
    pass
