from django.conf.urls import url, include
from django.db.models import base
from rest_framework import routers
from apps.chain.views import TxViewSet

router = routers.DefaultRouter()
router.register('tx', TxViewSet, basename='tx')

urlpatterns = [
    url(r'^', include(router.urls)),
]
