"""cpchain_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.conf.urls import url, handler404, handler500

from rest_framework_swagger.views import get_swagger_view

import xadmin
from index.views import *
from django.views.static import serve
from cpchain_test.settings import MEDIA_ROOT
from django.conf.urls.i18n import i18n_patterns

from cpchain_test.settings import SWAGGER_URL

schema_view = get_swagger_view(title='CPChain Website API')

indexpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('index_old', IndexView_Old.as_view(), name='index_old'),
    path('notification',NotificationView.as_view(),name='notification'),
    path('index_video',IndexVideoView.as_view(),name='index_video'),
    path('community/', CommunityView.as_view(), name='community'),
    path('developer/', DeveloperView.as_view(),name='developer'),
    path('news/list/<category>', NewsListView.as_view(), name='news_list'),
    path('rnode/', RnodeView.as_view(), name='rnode'),
    path('explorer/', include(('explorer.urls', 'explorer'), namespace='explorer')),
    path('wallet/', include(('wallet.urls', 'wallet'), namespace='wallet')),
    path('app/<app>', AppView.as_view(), name='app'),
    path('world_map/', WorldMapView.as_view(), name='world_map'),
    path('search/', include('haystack.urls')),
    path('password/',   PasswordView.as_view(), name='password'),
    # path('faucet/', FaucetView.as_view(), name='faucet'),
    path('receipt/', ReceiptView.as_view(), name='receipt'),
    path('proposal/', ProposalView.as_view(), name='proposal'),
    path('task/', TaskView.as_view(), name='task'),
    path('proposal/list/<types>', ProposalListView.as_view(), name='proposal_list'),
    path('proposal/detail/<proposal_id>', ProposalDetailView.as_view(), name='proposal_detail'),
    path('proposal/congress', CongressListView.as_view(), name='proposal_congress'),

 
    # functions
    # 配置富文本media地址
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('download/<paper>/', DownloadView.as_view(), name='download'),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

]

urlpatterns = i18n_patterns(
    path('', include('django_prometheus.urls')),
    path('', include(indexpatterns)),
    path('community-manage/', include('community.urls')),
    path('nodes/', include('node_ip.urls')),
    url(r'^api-docs$', schema_view),
    prefix_default_language=False
)

#
# # 上传的图片是到media中，不是在static中。我们还需要设置media可被访问，如下设置可用于开发中使用，若部署到服务器可用服务器软件设置
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
handler500 = server_error
