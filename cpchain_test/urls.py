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
from django.urls import path, include
import xadmin
from index.views import *

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('news', NewsView.as_view(), name='news'),
    # 配置富文本media地址
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('news_detail', NewsDetailView.as_view(), name='news_detail'),
    path('rnodes', RnodesView.as_view(), name='rnodes')
]

# 上传的图片是到media中，不是在static中。我们还需要设置media可被访问，如下设置可用于开发中使用，若部署到服务器可用服务器软件设置
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
