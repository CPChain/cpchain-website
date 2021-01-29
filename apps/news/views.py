"""

views

"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from cpc_fusion import Web3
from django_filters import compat

from common.pageable import PageableBackend

from apps.index.models import New, Media

from log import get_log

log = get_log('app')

# web3
class NewsBackend(BaseFilterBackend):

    def filter_queryset(self, request, qs, view):
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='category',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="类型"
                )
            ),
        ]


class NewsView(viewsets.ViewSet):
    queryset = New.objects.all()
    filter_backends = [PageableBackend, NewsBackend]

    def list(self, request):
        limit:int = request.GET.get('limit', 10)
        offset:int = request.GET.get('page', 0)
        
        data = {}
        return Response(data)
