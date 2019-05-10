from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from explorer import views

urlpatterns = [
    path('', views.explorer, name='explorer'),
    path('wshandler/', views.wshandler, name='wshandler'),
    path('blocks/', views.blocks, name='blocks'),
    path('block/<block_identifier>', views.block, name='block'),
    path('txs/', views.txs, name='txs'),
    path('tx/<tx_hash>', views.tx, name='tx'),
    path('address/<address>', views.address, name='address'),
    path('search/', views.search, name='search'),
    path('rnode/', views.rnode, name='rnode'),
    path('committee/',views.committee,name='committee'),
    path('event/<address>',views.event,name='event'),
    path('abi/<address>',csrf_exempt(views.abi),name='abi'),
    path('source/<address>',csrf_exempt(views.source),name='source'),
    path('stats/<address>',views.stats,name='stats'),
]
