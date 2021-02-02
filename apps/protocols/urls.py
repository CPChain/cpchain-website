from django.urls import path
from .views import PrivacyCNView, PrivacyZHView

urlpatterns = [
    path('privacy-cn/', PrivacyCNView.as_view(), name='privacy-cn'),
    path('privacy-zh/', PrivacyZHView.as_view(), name='privacy-zh'),
]
