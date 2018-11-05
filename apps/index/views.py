from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import FileResponse
from django.urls import reverse
from django.utils.translation import activate

from pure_pagination import Paginator, PageNotAnInteger

from .models import *
from urllib.parse import unquote


# Create your views here.
class IndexView(View):
    def get(self, req):
        partners = Partner.objects.filter(type='Partners')
        investors = Partner.objects.filter(type='Investors')
        exchanges = Partner.objects.filter(type='Exchanges')
        main_teams =TeamMate.objects.filter(is_main=True)
        global_teams = TeamMate.objects.filter(is_main=False)
        return render(req, 'index.html', locals())


class LangView(View):
    def get(self, req):
        lang = req.GET.get("lang")
        activate(lang)
        return redirect(reverse('index'))


class NewsView(View):
    def get(self, req):
        title = req.GET.get('title', '')
        if title:
            # get the detail page
            title = unquote(title)
            news = New.objects.filter(title=title)[0]
            latest_news = New.objects.filter(category=news.category).exclude(title=title).order_by('-update_time')[:3]
            return render(req, 'news_detail.html', {'news': news, 'latest': latest_news})
        else:
            # index
            community_update_news = New.objects.filter(category='Community Updates').order_by('-update_time')[:3]
            ama_news = New.objects.filter(category='AMA Sessions').order_by('-update_time')[:3]
            media_reports_news = New.objects.filter(category='Media Reports').order_by('-update_time')[:3]
            return render(req, 'news.html',
                          {'CU_news': community_update_news, 'ama_news': ama_news, 'media_news': media_reports_news})



class NewsListView(View):
    def get(self, req, category):
        category = unquote(category)
        news_with_category = New.objects.filter(category=category)
        try:
            page = req.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        all_news = news_with_category
        p = Paginator(all_news, 12, request=req)
        news = p.page(page)
        return render(req, 'news_list.html', {'category': category, 'news': news})


class RnodeView(View):
    def get(self, req):
        return render(req, 'rnode.html')


class DownloadView(View):
    def get(self, req, paper):
        file = open('static/' + paper, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(paper)
        return response


class AppView(View):
    def get(self, req, app):
        return render(req, app + '.html')



def page_not_found(request):
    return render(request, 'errors/page_404.html')


def server_error(request):
    return render(request, 'errors/page_500.html')