from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path(r'login/', obtain_auth_token, name='login'),  # <-- And here
    path(r'hello/', views.HelloView.as_view(), name='hello'),
]
