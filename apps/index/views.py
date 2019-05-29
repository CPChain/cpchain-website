from urllib.parse import unquote

from cpc_fusion import Web3
from django.http import FileResponse, HttpResponseRedirect
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
        partners = Partner.objects.filter(type='Partners').order_by('-weight')
        # print(partners)
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
                official_announcement_news = New.objects.filter(category='Official Announcement').order_by(
                    '-update_time')[:3]
                community_update_news = New.objects.filter(category='Community Updates').order_by('-update_time')[:3]
                community_events_news = New.objects.filter(category='Community Events').order_by('-update_time')[:3]
                media_reports_news = Media.objects.filter(category='Media Reports').order_by('-update_time')[:3]
                return render(req, 'community.html',
                              {'OA_news': official_announcement_news, 'CU_news': community_update_news,
                               'community_events_news': community_events_news,
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
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline;filename="{}"'.format(paper)
        return response


class AppView(View):
    def get(self, req, app):
        return render(req, app + '.html')


class PasswordView(View):
    def get(self, req):
        if 'faucet' in req.COOKIES and ':' in req.COOKIES['faucet']:
            cookie = req.get_signed_cookie('faucet', salt="cpc")
            if cookie == 'login':
                return redirect('faucet')
        return render(req, 'password.html')

    def post(self, req):
        password = req.POST.get('password', '')
        if not password:
            if not req.path.startswith('/zh-hans'):
                return render(req, 'password.html', {'msg': "Please input a password."})
            return render(req, 'password.html', {'msg': "请输入密码"})
        else:
            if password == 'cpchain2019':
                # return redirect('faucet')
                response = HttpResponseRedirect('/faucet')
                response.set_signed_cookie('faucet', 'login', salt="cpc", max_age=60 * 30, httponly=True)
                return response
            else:
                if not req.path.startswith('/zh-hans'):
                    return render(req, 'password.html', {'msg': "Incorrect password."})
                return render(req, 'password.html', {'msg': "密码错误"})


class FaucetView(View):
    def get(self, req):
        if 'faucet' in req.COOKIES and ':' in req.COOKIES['faucet']:
            cookie = req.get_signed_cookie('faucet', salt="cpc")
            if cookie == 'login':
                return render(req, 'faucet.html')
        return redirect('password')

    def post(self, req):
        if 'faucet' in req.COOKIES and ':' in req.COOKIES['faucet']:
            cookie = req.get_signed_cookie('faucet', salt="cpc")
            if cookie == 'login':
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
                            return render(req, 'faucet.html',
                                          {'msg': 'The limitation of daily faucet has been reached. '})
                        return render(req, 'faucet.html', {'msg': '您已经达到了今天的测试币申领额度上限'})
                else:
                    if not req.path.startswith('/zh-hans'):
                        return render(req, 'faucet.html', {'msg': 'Please enter a valid wallet address.'})
                    return render(req, 'faucet.html', {'msg': '请输入一个有效钱包地址'})
        return redirect('password')


class ReceiptView(View):
    def get(self, req):
        return render(req, 'faucet-receipt.html')


def page_not_found(request, exception=None, template_name='errors/page_404.html'):
    return render(request, template_name)


def server_error(request, exception=None, template_name='errors/page_500.html'):
    return render(request, template_name)
