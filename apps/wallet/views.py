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
        events_list = WalletNew.objects.filter(category='Event_en')
    elif lang == 'cn':
        events_list = WalletNew.objects.filter(category='Event_cn')

    msg = serializers.serialize('json', events_list,
                                fields=('pk', 'category', 'title', 'banner', 'update_time'))
    return JsonResponse(msg, safe=False)


def news_list(req, lang):
    if lang == 'en':
        news_list = WalletNew.objects.filter(category='News_en')
    elif lang == 'cn':
        news_list = WalletNew.objects.filter(category='News_cn')

    data = serializers.serialize("json", news_list,
                                 fields=('pk', 'category', 'title', 'banner', 'update_time'))
    # data_dict = json.dumps(data)
    return JsonResponse(data, safe=False)


def swipe(req, lang):
    banner = SwipeBanner.objects.filter(lang=lang)
    print(banner)
    data = serializers.serialize("json", banner, )
    return JsonResponse(data, safe=False)
