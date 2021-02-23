from django.conf.urls import url, include
from django.db.models import base
from rest_framework import routers
from apps.chain.views import RNodeStatusViewSet, TxViewSet, RNodeRewardViewSet, RewardHistoryView

router = routers.DefaultRouter()
router.register('tx', TxViewSet, basename='tx')
router.register('rnodes-reward', RNodeRewardViewSet, basename='rnodes-reward')
router.register('rnode-status', RNodeStatusViewSet, basename='rnode-status')
router.register('reward-history', RewardHistoryView, basename='reward-history')

urlpatterns = [
    url(r'^', include(router.urls)),
]
