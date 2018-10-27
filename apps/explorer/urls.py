from django.urls import path
from explorer import views

urlpatterns = [
    path('', views.explorer,name='index'),
    path('wshandler/', views.wshandler),
    path('blocks/', views.blocks),
    path('block/<block_identifier>', views.block),
    path('txs/', views.txs),
    path('tx/<tx_hash>', views.tx),
    path('address/<address>', views.address),
    path('contract/<contract>', views.contract),
    path('search/', views.search),
]
