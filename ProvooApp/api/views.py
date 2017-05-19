from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User


# Create your views here.


class PruebaApi(APIView):
    def get(self, request, format=None):
        return Response({'message: Hola Mundo Response de Framework APi rest'})


class UserApi(APIView):
    serializers_class = UserSerializer

    def get(self, request, format=None):
        users = User.objects.all()
        response = self.serializers_class(users, many=True)
        return Response(response.data)
