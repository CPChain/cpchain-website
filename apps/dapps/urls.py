from django.conf.urls import url, include
from django.db.models import base
from rest_framework import routers
from apps.dapps.views import MessageDAppView

router = routers.DefaultRouter()
router.register('message', MessageDAppView, basename='message')

urlpatterns = [
    url(r'^', include(router.urls)),
]
