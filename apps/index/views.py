from urllib.parse import unquote

from cpc_fusion import Web3
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.base import View
from pure_pagination import PageNotAnInteger, Paginator

from cpchain_test.config import cfg

from .faucet import Faucet
from .models import *
from .tasks import faucet

chain = 'http://{0}:{1}'.format(cfg['faucet']['ip'], cfg['faucet']['port'])
cf = Web3(Web3.HTTPProvider(chain))


# Create your views here.
class IndexView(View):
    def get(self, req):
        partners = Partner.objects.filter(type='Partners')
        investors = Partner.objects.filter(type='Investors')
        exchanges = Partner.objects.filter(type='Exchanges')
        main_teams = TeamMate.objects.filter(is_main=True)
        global_teams = TeamMate.objects.filter(is_main=False)
        return render(req, 'index.html', locals())



class CommunityView(View):
    def get(self, req):
        title = req.GET.get('title', '')
        if title:
            # get the detail page
            title = unquote(title)
            news = New.objects.filter(title=title)[0]
            latest_news = New.objects.filter(category=news.category).exclude(title=title).order_by('-update_time')[:3]
            return render(req, 'news_detail.html', {'news': news, 'latest': latest_news})
        else:
            # eng version
            if not req.path.startswith('/zh-hans'):
                official_announcement_news = New.objects.filter(category='Official Announcement').order_by('-update_time')[:3]
                community_update_news = New.objects.filter(category='Community Updates').order_by('-update_time')[:3]
                community_events_news = New.objects.filter(category='Community Events').order_by('-update_time')[:3]
                media_reports_news = Media.objects.filter(category='Media Reports').order_by('-update_time')[:3]
                return render(req, 'community.html',
                              {'OA_news':official_announcement_news,'CU_news': community_update_news, 'community_events_news': community_events_news,
                               'media_news': media_reports_news})

            else:
                # zh version
                progress_news = New.objects.filter(category='项目进展').order_by('-update_time')[:3]
                release_news = New.objects.filter(category='重大发布').order_by('-update_time')[:3]
                media_news = Media.objects.filter(category='媒体报道').order_by('-update_time')[:3]
                return render(req, 'community_zh.html',
                              {'progress_news': progress_news, 'release_news': release_news, 'media_news': media_news})


class DeveloperView(View):
    def get(self, req):
        return HttpResponseRedirect('http://docs.cpchain.io')


class NewsListView(View):
    def get(self, req, category):
        category = unquote(category)
        if not category in ['Media Reports', '媒体报道']:
            news_with_category = New.objects.filter(category=category).order_by('-update_time')
            try:
                page = req.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            all_news = news_with_category
            p = Paginator(all_news, 12, request=req)
            news = p.page(page)
            return render(req, 'news_list.html', {'category': category, 'news': news})
        else:
            media_category = Media.objects.filter(category=category).order_by('-update_time')
            try:
                page = req.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            all_news = media_category
            p = Paginator(all_news, 12, request=req)
            media_news = p.page(page)
            return render(req, 'news_list.html', {'category': category, 'media_news': media_news})


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



class FaucetView(View):
    def get(self, req):
        return render(req, 'faucet.html')

    def post(self, req):
        # locale
        address = req.POST.get('address', '')
        address = address.strip()
        if cf.isAddress(address):
            if Faucet.valid():
                if Faucet.limit(address):
                    faucet.delay(address)
                    return redirect('receipt')
                else:
                    if not req.path.startswith('/zh-hans'):
                        return render(req, 'faucet.html', {'msg': "You have already claimed today's faucet."})
                    return render(req, 'faucet.html', {'msg': "您已经申领今天的测试币"})
            else:
                if not req.path.startswith('/zh-hans'):
                    return render(req, 'faucet.html', {'msg': 'The limitation of daily faucet has been reached. '})
                return render(req, 'faucet.html', {'msg': '您已经达到了今天的测试币申领额度上限'})
        else:
            if not req.path.startswith('/zh-hans'):
                return render(req, 'faucet.html', {'msg': 'Please enter a valid wallet address.'})
            return render(req, 'faucet.html', {'msg': '请输入一个有效钱包地址'})


class ReceiptView(View):
    def get(self, req):
        return render(req, 'faucet-receipt.html')


def page_not_found(request, exception=None, template_name='errors/page_404.html'):
    return render(request, template_name)


def server_error(request, exception=None, template_name='errors/page_500.html'):
    return render(request, template_name)
