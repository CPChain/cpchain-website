"""

views

"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from django_filters import compat

from haystack.views import SearchView

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
                    description="文章类型: " +
                    ", ".join([f'"{i[0]}"' for i in NEWS_CATEGORY])
                )
            ),
        ]


class NewsView(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin):
    queryset = New.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [NewsBackend, ]

    def get_serializer_class(self):
        if self.action in ['list']:
            return NewsListSerializer
        return super().get_serializer_class()

class MySearchView(SearchView):

    # def get_extra_actions():
    #     return None

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        
        context:
        + 'query': self.query,
        + 'form': self.form,
        + 'page': page,
        + 'paginator': paginator,
        + 'suggestion': None,
        """
        context = self.get_context()
        page = context['page']
        paginator = context['paginator']
        results = [dict(banner=str(i.object.banner), category=i.object.category, title=i.object.title,
                        update_time=i.object.update_time.strftime('%Y-%m-%d'), summary=i.object.summary) for i in page.object_list]
        return Response({
            "count": paginator.count,
            "page": page.number,
            "results": results
        })


class NewsSearchPageableBackend(BaseFilterBackend):

    def filter_queryset(self, request, qs, view):
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='q',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="查询关键词"
                )
            ),
            compat.coreapi.Field(
                name='page',
                required=False,
                type="int",
                location='query',
                schema=compat.coreschema.String(
                    description="页数"
                )
            ),
        ]

class NewsSearchView(viewsets.ViewSet):
    """
    通过 django-haystack 提供查询功能，每页大小固定为 12
    """
    filter_backends = [NewsSearchPageableBackend]

    def list(self, request):
        return MySearchView()(request)
