from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from .views import TasksViewSet, ProposalsViewSet, CongressViewSet, \
    ApprovedAddressViewSet, VotedAddressViewSet, ProposalTypeViewSet, ContractViewSet, TaskClaimViewSet, \
    ConfigViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'tasks', TasksViewSet)
router.register(r'task/claim', TaskClaimViewSet)
router.register(r'contract', ContractViewSet)
router.register(r'contract/config', ConfigViewSet)
router.register(r'proposals', ProposalsViewSet)
router.register(r'congress', CongressViewSet)
router.register(r'likes', ApprovedAddressViewSet)
router.register(r'votes', VotedAddressViewSet)
router.register(r'proposal-type', ProposalTypeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
