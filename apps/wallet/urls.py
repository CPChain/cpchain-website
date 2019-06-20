from django.urls import path
from wallet.views import *

urlpatterns = [
    path('news_detail/<pk>', news_detail),
    path('news_list/<lang>', news_list),
    path('news_detail/<pk>', event_detail),
    path('events_list/<lang>', event_list),
]
