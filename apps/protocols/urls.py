from django.urls import path
from .views import PrivacyCNView

urlpatterns = [
    path('privacy-cn/', PrivacyCNView.as_view(), name='privacy-cn'),
]
