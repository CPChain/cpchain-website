from django.urls import path
from .views import news_detail, news_list, events_list, swipe

urlpatterns = [
    path('news_detail/<pk>', news_detail),
    path('news_list/<lang>', news_list),
    path('events_list/<lang>', events_list),
    path('get_banner/<lang>', swipe)
]
