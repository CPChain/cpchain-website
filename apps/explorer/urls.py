from django.urls import path
from explorer import views

urlpatterns = [
    path('', views.explorer,name='explorer'),
    path('wshandler/', views.wshandler,name='wshandler'),
    path('blocks/', views.blocks,name='blocks'),
    path('block/<block_identifier>', views.block,name='block'),
    path('txs/', views.txs,name='txs'),
    path('tx/<tx_hash>', views.tx,name='tx'),
    path('address/<address>', views.address,name='address'),
    path('contract/<contract>', views.contract,name='contract'),
    path('search/', views.search,name='exp_search'),
]
