from django.urls import path
from .views import PrivacyCNView, PrivacyZHView

urlpatterns = [
    path('privacy-en/', PrivacyCNView.as_view(), name='privacy-en'),
    path('privacy-zh/', PrivacyZHView.as_view(), name='privacy-zh'),
]
