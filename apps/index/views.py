from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import *


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
        return render(req, 'news.html')


class NewsDetailView(View):
    def get(self, req):
        news = New.objects.all()
        return render(req, 'news_detail.html', {'news': news})


class RnodesView(View):
    def get(self, req):
       return HttpResponse('rnodes')