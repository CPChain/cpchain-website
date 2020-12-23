from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path(r'login/', obtain_auth_token, name='login'),
    path(r'info/', views.UserInfoView.as_view(), name='info'),
    path(r'hello/', views.HelloView.as_view(), name='hello'),
    path(r'logout/', views.LogoutView.as_view(), name='logout')
]
