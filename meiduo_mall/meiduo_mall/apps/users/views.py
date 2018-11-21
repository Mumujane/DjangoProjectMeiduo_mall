from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from . import serializers


# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class UsernameCountView(APIView):
    """
    用户名数量
    """

    def get(self, request, username):
        """
        获取指定用户名数量

        :param request:
        :param username:
        :return:
        """
        count = User.objects.filter(username=username).count()
        data = {
            'username': username,
            'count': count,
        }
        print("!1111")
        return Response(data)


class MobileCountView(APIView):
    """手机号"""

    def get(self, request, mobile):
        """

        :param request:
        :param mobile:
        :return:
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


# url(r'^users/$', views.UserView.as_view())
class UserView(CreateAPIView):
    """
    用户注册
    """

    serializer_class = serializers.CreateUserSerializer

