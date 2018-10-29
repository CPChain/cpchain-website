from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import *
from urllib.parse import unquote


# Create your views here.
class IndexView(View):
    def get(self, req):
        search = req.GET.get('s')
        if not search:
            return render(req, 'index.html')
        else:
            return HttpResponse(search)


class NewsView(View):
    def get(self, req):
        community_update_news = New.objects.filter(category='Community Updates').order_by('-update_time')[:3]
        ama_news = New.objects.filter(category='AMA Sessions').order_by('-update_time')[:3]
        media_reports_news = New.objects.filter(category='Media Reports').order_by('-update_time')[:3]
        return render(req, 'news.html',
                      {'CU_news': community_update_news, 'ama_news': ama_news, 'media_news': media_reports_news})


class NewsDetailView(View):
    def get(self, req, title):
        title = unquote(title)
        news = New.objects.filter(title=title)[0]
        latest_news = New.objects.filter(category=news.category).exclude(title=title).order_by('-update_time')[:3]
        return render(req, 'news_detail.html', {'news': news, 'latest': latest_news})


class RnodesView(View):
    def get(self, req):
        return HttpResponse('rnodes')
