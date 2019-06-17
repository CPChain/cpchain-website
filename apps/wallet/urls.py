from django.urls import path
from wallet.views import *

urlpatterns = [
    path('', community_detail),
]
