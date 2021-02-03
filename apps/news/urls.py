from django.conf.urls import url, include
from rest_framework import routers
from apps.news.views import NewsView, NewsSearchView

router = routers.DefaultRouter()
router.register('news', NewsView, basename='news')
router.register('search', NewsSearchView, basename='search')

urlpatterns = [
    url(r'^', include(router.urls)),
]
