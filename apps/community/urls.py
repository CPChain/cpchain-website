from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from .views import TasksViewSet, ProposalsViewSet, ProposalsUpdateViewSet, ProposalsCreateViewSet, CongressViewSet, \
    ApprovedAddressViewSet, VotedAddressViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'tasks', TasksViewSet)
router.register(r'proposals', ProposalsViewSet)
router.register(r'proposals', ProposalsUpdateViewSet, basename='update status of proposal by admin')
router.register(r'proposals', ProposalsCreateViewSet, basename='create proposal')
router.register(r'congress', CongressViewSet)
router.register(r'likes', ApprovedAddressViewSet)
router.register(r'votes', VotedAddressViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
