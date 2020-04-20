
from rest_framework import permissions
from datetime import datetime as dt

from .models import IPAccess
from .serializers import IPAccessSerializer

class IPLimitPermission(permissions.BasePermission):
    message = "You posted too many requests today."
    limit = 5

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        url = request.META['PATH_INFO']
        if url in ['/api-docs']:
            return True
        ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
        # check
        blocklisted = IPAccess.objects.filter(IP=ip, url=url, date=dt.now().date()).count() >= self.limit
        if not blocklisted:
            # add record
            serializer = IPAccessSerializer(data=dict(IP=ip, url=url, date=dt.now().date()))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        return not blocklisted
