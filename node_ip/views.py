"""

views.py

"""

from rest_framework import viewsets, mixins

from .models import IP
from .serializers import IPSerializer


class IPViewSet(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """ CPChain 节点分布
    """
    queryset = IP.objects.filter(handled=True, deleted=False)
    serializer_class = IPSerializer
