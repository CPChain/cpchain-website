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
    path('proposers/', views.proposers, name='proposers'),
    path('proposers/history/', views.committeeHistory, name='committeeHistory'),
    path('event/<address>', views.event, name='event'),
    path('proposer_history/<address>', views.proposer_history, name='proposer_history'),
    path('abi/<address>', csrf_exempt(views.abi), name='abi'),
    path('source/<address>', csrf_exempt(views.source), name='source'),
    # dev
    path('impeachs_by_addr/<address>/', views.impeachs_by_addr, name='impeachs_by_addr'),
    path('impeachs_by_block/<block>/<isOur>', views.impeachs_by_block, name='impeachs_by_block'),
    path('all_blocks/', views.all_blocks, name='impeachs_by_block'),
    path('check_campaign/', views.check_campaign, name='campaign_history'),
    path('candidate_info/<addr>', views.candidate_info, name='candidate_info'),
    path('impeachFrequency/', views.impeachFrequency,name='impeachFrequency'),
]
