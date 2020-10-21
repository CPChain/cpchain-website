
from rest_framework import viewsets, mixins

from .models import Suggest
from .serializers import SuggestSerializer


class SuggestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ 提交建议
    """
    queryset = Suggest.objects.filter()
    serializer_class = SuggestSerializer

