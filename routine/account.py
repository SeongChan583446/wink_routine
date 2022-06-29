from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *

class SignupView(APIView):
    def post(self, request):
        user = User.objects.create_user(
            email = request.data['email'],
            username=request.data['username'],
            password=request.data['password'])
        profile = Profile(user=user)

        user.save()
        profile.save()

        token = Token.objects.create(user=user)
        return Response({"Token": token.key})

class LoginView(APIView):
    def post(self, request):
        user=authenticate(username=request.data['username'], password=request.data['password'])
        if user is None:
            return Response(status=401)
        else:
            token = Token.objects.get(user=user)
            response = {
                "Token": token.key
            }
            return Response(response)