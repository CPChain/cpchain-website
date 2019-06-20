from django.urls import path
from wallet.views import *

urlpatterns = [
    path('news_detail/<pk>', news_detail),
    path('news_list/<lang>', news_list),
    path('events_list/<lang>', events_list),
]
