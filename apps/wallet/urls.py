from django.urls import path

from .views import news_detail, news_list, events_list, swipe, faq_list, faq_detail, term_detail,download_app,rule_detail

urlpatterns = [
    path('news_detail/<pk>', news_detail),
    path('news_list/<lang>', news_list),
    path('events_list/<lang>', events_list),
    path('get_banner/<lang>', swipe),
    path('faq_list/<lang>', faq_list),
    path('faq_detail/<pk>', faq_detail),
    path('term_detail/<lang>/<title>', term_detail),
    path('rule_detail/<title>', rule_detail),
    path('download_app/', download_app),
]
