from django.conf.urls import url, include
from rest_framework import routers

from .views import TemplateViewSet, TemplateTypeViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'template-type', TemplateTypeViewSet)
router.register(r'template', TemplateViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
