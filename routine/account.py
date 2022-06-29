from typing import OrderedDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *

import json

class SignupView(APIView):
    def post(self, request):
        response = OrderedDict()
        response["message"] = OrderedDict()
        password = request.data['password']
        if len(password) < 8:
            response["message"]["msg"] = "password is too short."
            response["message"]["status"] = "SIGNUP_FAIL"
            json.dumps(response, ensure_ascii=False, indent="\t")

            return Response(response)
        
        flag_num = False
        flag_spe = False
        num_arr = ['0','1','2','3','4','5','6','7','8','9']
        spe_arr = ['!','@','#','$','%','^','&','*','(',')','_','+']
        for i in range(len(password)):
            if password[i] in num_arr:
                flag_num = True
            if password[i] in spe_arr:
                flag_spe = True
        
        if flag_num == False:
            response["message"]["msg"] = "password is not include number."
            response["message"]["status"] = "SIGNUP_FAIL"
            json.dumps(response, ensure_ascii=False, indent="\t")

            return Response(response)
        
        if flag_spe == False:
            response["message"]["msg"] = "password is not include special words."
            response["message"]["status"] = "SIGNUP_FAIL"
            json.dumps(response, ensure_ascii=False, indent="\t")

            return Response(response)


        user = User.objects.create_user(
            email = request.data['email'],
            username=request.data['username'],
            password=password)
        profile = Profile(user=user)

        user.save()
        profile.save()

        token = Token.objects.create(user=user)
        response["message"]["msg"] = " ."
        response["message"]["status"] = "SIGNUP_OK"

        json.dumps(response, ensure_ascii=False, indent="\t")

        return Response(response)

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