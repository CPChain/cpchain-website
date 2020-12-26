"""

user

"""
from rest_framework import status
from rest_framework import generics
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class HelloView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class UserInfoView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({
            "username": request.user.username,
            "avatar": "static/img/favicon.ico",
        })

class LogoutView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.Serializer

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
