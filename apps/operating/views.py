"""

operating views

"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Templates, TemplateType
from .serializers import TemplateSerializer, TemplateTypeSerializer

class TemplateTypeViewSet(viewsets.ModelViewSet):
    queryset = TemplateType.objects.filter()
    serializer_class = TemplateTypeSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Templates.objects.filter()
    serializer_class = TemplateSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
