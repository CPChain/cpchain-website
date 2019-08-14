from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from urllib.parse import unquote

from .models import *


# Create your views here.
def term_detail(req,lang, title):
    title = unquote(title)
    term = Term.objects.get(title=title)
    if lang == 'en':
        return render(req, 'wallet/term.html', locals())
    else:
        return render(req, 'wallet/term_cn.html', locals())


def faq_detail(req, pk):
    faq = FAQ.objects.get(pk=pk)
    return render(req, 'wallet/faq_detail.html', locals())


def news_detail(req, pk):
    news = WalletNew.objects.get(pk=pk)
    return render(req, 'wallet/news_detail.html', locals())


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


def faq_list(req, lang):
    if lang == 'en':
        faq_list = FAQ.objects.filter(lang='en')
    elif lang == 'zh':
        faq_list = FAQ.objects.filter(lang='zh')

    data = serializers.serialize("json", faq_list,
                                 fields=('pk', 'title', 'weight'))
    # data_dict = json.dumps(data)
    return JsonResponse(data, safe=False)


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
    banner = SwipeBanner.objects.filter(lang=lang, is_active=True).order_by('-banner_time')
    data = serializers.serialize("json", banner)
    return JsonResponse(data, safe=False)
