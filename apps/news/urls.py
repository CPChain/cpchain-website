from django.conf.urls import url, include
from rest_framework import routers
from apps.news.views import NewsView

router = routers.DefaultRouter()
router.register('news', NewsView, basename='news')

urlpatterns = [
    url(r'^', include(router.urls)),
]
