from django.urls import path
from wallet.views import *

urlpatterns = [
    path('news_detail/<pk>', community_detail),
]
