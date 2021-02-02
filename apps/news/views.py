"""

views

"""

from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend
from django_filters import compat

from apps.index.models import New, NEWS_CATEGORY
from .serializers import NewsSerializer, NewsListSerializer

from log import get_log

log = get_log('app')

# web3
class NewsBackend(BaseFilterBackend):

    def filter_queryset(self, request, qs, view):
        category = request.GET.get('category')
        if category and category.strip() != "":
            return qs.filter(category=category)
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='category',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="文章类型: " + ", ".join([f'"{i[0]}"' for i in NEWS_CATEGORY])
                )
            ),
        ]


class NewsView(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin):
    queryset = New.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [NewsBackend,]

    def get_serializer_class(self):
        if self.action in ['list']:
            return NewsListSerializer
        return super().get_serializer_class()
