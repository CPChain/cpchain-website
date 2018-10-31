from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.http import FileResponse

from .models import *
from urllib.parse import unquote


# Create your views here.
class IndexView(View):
    def get(self, req):
        exchanges = Partner.objects.filter(type='Exchanges')
        return render(req, 'index.html',locals())



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


class RnodeView(View):
    def get(self, req):
        return HttpResponse('rnode')


class DownloadView(View):
    def get(self, req, paper):
        file = open('static/' + paper, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(paper)
        return response
