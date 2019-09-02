from urllib.parse import unquote

from cpc_fusion import Web3
from django.http import FileResponse, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from pure_pagination import PageNotAnInteger, Paginator
from django.core import serializers

from cpchain_test.config import cfg
from .faucet import Faucet
from .models import *
import re

chain = 'http://{0}:{1}'.format(cfg['faucet']['ip'], cfg['faucet']['port'])
cf = Web3(Web3.HTTPProvider(chain))


# Create your views here.
def judge_pc_or_mobile(ua):
    """
    判断访问来源是pc端还是手机端
    :param ua: 访问来源头信息中的User-Agent字段内容
    :return:
    """
    factor = ua
    is_mobile = False
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp' \
                    r'|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)' \
                    r'|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)' \
                     r'|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)' \
                     r'|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw' \
                     r'|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8' \
                     r'|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit' \
                     r'|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)' \
                     r'|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji' \
                     r'|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx' \
                     r'|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi' \
                     r'|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)' \
                     r'|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg' \
                     r'|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21' \
                     r'|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-' \
                     r'|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it' \
                     r'|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)' \
                     r'|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)' \
                     r'|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit' \
                     r'|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'

    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(factor) != None:
        is_mobile = True
    user_agent = factor[0:4]
    if _short_matches.search(user_agent) != None:
        is_mobile = True

    return is_mobile

def reshape(arr,num):
    pages =[]
    for index in range(int(len(arr)/num) +1):
       pages.append(arr[index*num:(index+1)*num])
    return pages

class IndexView(View):
    def get(self, req):
        ua = req.META.get('HTTP_USER_AGENT', None)
        # 判断是否手机端，是则取消首页视频
        is_mobile = judge_pc_or_mobile(ua)
        partners = Partner.objects.filter(type='Partners').order_by('-weight')
        investors = Partner.objects.filter(type='Investors')
        exchanges = reshape(Partner.objects.filter(type='Exchanges'),6)
         
        industry = reshape(Partner.objects.filter(type='Industry'),6)

        project =  reshape(Partner.objects.filter(type='Project'),6)
        academia =  reshape(Partner.objects.filter(type='Academia'),6)
        capital =  reshape(Partner.objects.filter(type='Capital'),6)
        association =  reshape(Partner.objects.filter(type='Association') ,6)
        industryNode =  reshape(Partner.objects.filter(type='IndustryNode') ,6)
        main_teams =  TeamMate.objects.filter(is_main=True)
        global_teams =  TeamMate.objects.filter(is_main=False) 
        # notification = Notification.objects.all()
        videos = []
        return render(req, 'index.html', locals())


class NotificationView(View):
    def get(self, req):
        data = serializers.serialize('json', Notification.objects.all(), )
        return HttpResponse(data)


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
