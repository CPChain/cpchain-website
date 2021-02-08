"""

pageable filter

"""
from rest_framework.filters import BaseFilterBackend
from cpc_fusion import Web3
from django_filters import compat

class PageableBackend(BaseFilterBackend):

    def filter_queryset(self, request, qs, view):
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='limit',
                required=False,
                type="int",
                location='query',
                schema=compat.coreschema.String(
                    description="每页大小"
                )
            ),
            compat.coreapi.Field(
                name='page',
                type="int",
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="页数，从1开始"
                )
            ),
        ]
