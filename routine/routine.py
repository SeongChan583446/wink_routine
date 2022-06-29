from typing import OrderedDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *

import json, datetime

def find_days(days):
    result = []
    if days.find("MON") != -1:
        result.append("MON")
    if days.find("TUE") != -1:
        result.append("TUE")
    if days.find("WED") != -1:
        result.append("WED")
    if days.find("THU") != -1:
        result.append("THU")
    if days.find("FRI") != -1:
        result.append("FRI")
    if days.find("SAT") != -1:
        result.append("SAT")
    if days.find("SUN") != -1:
        result.append("SUN")

    return result

class CreateRoutineView(APIView):
    def post(self, request):
        user = request.user
        user_token = request.auth

        #token으로 유저 식별
        token = Token.objects.get(user = user)
        if token.key != user_token.key:
            return Response(status=401)
        else:
            title = request.data["title"]
            category = request.data['category']
            goal = request.data['goal']
            alarm = request.data['is_alarm']
            days = request.data['days']

            days_arr = find_days(days)
            if alarm == "True":
                is_alarm = True
            else:
                is_alarm = False

            #routine생성
            routine = Routine.objects.create(
                account_id = user.id,
                title = title,
                category = category,
                goal = goal,
                is_alarm = is_alarm
            )
            routine.save()

            #result 생성
            routine_result = RoutineResult.objects.create(
                routine_id = routine,
                result = "NOT"
            )
            routine_result.save()

            #day 추가
            for i in range(len(days_arr)):
                routine_day = RoutineDay.objects.create(
                    day = days_arr[i],
                    routine_id = routine
                )
                routine_day.save()

            #response
            response = OrderedDict()
            response["data"] = OrderedDict()
            response["data"]["routine_id"] = routine.routine_id
            response["message"] = OrderedDict()
            response["message"]["msg"] = " ."
            response["message"]["status"] = "ROUTINE_CREATE_OK"

            json.dumps(response, ensure_ascii=False, indent="\t")
            return Response(response)

class InquireRoutineListView(APIView):
    def get(self, request):
        user = request.user
        user_token = request.auth

        #token으로 유저 식별
        token = Token.objects.get(user = user)
        if token.key != user_token.key:
            return Response(status=401)
        else:
            account_id = request.data["account_id"]
            today = request.data['today']
            day = self.date_to_day(today)

            routine_day = RoutineDay.objects.filter(day = day)
            
            #response
            response = OrderedDict()
            response["data"] = [0 for i in range(len(routine_day))]

            for i in range(len(routine_day)):
                routine = Routine.objects.get(account_id = account_id, routine_id = routine_day[0].routine_id.routine_id)
                routine_result = RoutineResult.objects.get(routine_id = routine)
                
                response["data"][i] = OrderedDict()
                response["data"][i]["goal"] = routine.goal
                response["data"][i]["id"] = routine.account_id
                response["data"][i]["result"] = routine_result.result
                response["data"][i]["title"] = routine.title

            response["message"] = OrderedDict()
            response["message"]["msg"] = " ."
            response["message"]["status"] = "ROUTINE_LIST_OK"

            json.dumps(response, ensure_ascii=False, indent="\t")
        
            return Response(response)
        
    def date_to_day(self, date):
        
        today = list(map(int,date.split('-')))
        today_num = datetime.date(today[0],today[1],today[2]).weekday()

        result = ""
        if today_num == 0:
            result = "MON"
        elif today_num == 1:
            result = "THU"
        elif today_num == 2:
            result = "WED"
        elif today_num == 3:
            result = "THU"
        elif today_num == 4:
            result = "FRI"
        elif today_num == 5:
            result = "SAT"
        elif today_num == 6:
            result = "SUN"
        
        return result


class InquireRoutineView(APIView):
    def get(self, request):
        user = request.user
        user_token = request.auth

        #token으로 유저 식별
        token = Token.objects.get(user = user)
        if token.key != user_token.key:
            return Response(status=401)
        else:
            account_id = request.data["account_id"]
            routine_id = request.data["routine_id"]

            routine = Routine.objects.get(account_id = account_id, routine_id = routine_id)
            routine_result = RoutineResult.objects.get(routine_id = routine)
            routine_day = RoutineDay.objects.filter(routine_id = routine)
            
            #response
            response = OrderedDict()            
                
            response["data"] = OrderedDict()
            response["data"]["goal"] = routine.goal
            response["data"]["id"] = routine.account_id
            response["data"]["result"] = routine_result.result
            response["data"]["title"] = routine.title

            days = []
            for i in range(len(routine_day)):
                days.append(routine_day[i].day)
            response["data"]["days"] = days

            response["message"] = OrderedDict()
            response["message"]["msg"] = " ."
            response["message"]["status"] = "ROUTINE_DETAIL_OK"

            json.dumps(response, ensure_ascii=False, indent="\t")
        
            return Response(response)

class UpdateRoutineView(APIView):
    def put(self, request):
        user = request.user
        user_token = request.auth

        #token으로 유저 식별
        token = Token.objects.get(user = user)
        if token.key != user_token.key:
            return Response(status=401)
        else:
            routine_id = request.data["routine_id"]
            title = request.data["title"]
            category = request.data['category']
            goal = request.data['goal']
            alarm = request.data['is_alarm']
            days = request.data['days']

            days_arr = find_days(days)
            if alarm == "True":
                is_alarm = True
            else:
                is_alarm = False

            #routine수정
            routine = Routine.objects.get(routine_id = routine_id)
            routine.title = title
            routine.category = category
            routine.goal = goal
            routine.is_alarm = is_alarm

            routine.save()

            #day삭제
            routine_day = RoutineDay.objects.filter(routine_id = routine)
            routine_day.delete()

            #삭제 후 재생성
            for i in range(len(days_arr)):
                routine_day = RoutineDay.objects.create(
                    day = days_arr[i],
                    routine_id = routine
                )
                routine_day.save()

            #response
            response = OrderedDict()
            response["data"] = OrderedDict()
            response["data"]["routine_id"] = routine.routine_id
            response["message"] = OrderedDict()
            response["message"]["msg"] = " ."
            response["message"]["status"] = "ROUTINE_UPDATE_OK"

            json.dumps(response, ensure_ascii=False, indent="\t")

            return Response(response)

class DeleteRoutineView(APIView):
    def delete(self, request):
        user = request.user
        user_token = request.auth

        #token으로 유저 식별
        token = Token.objects.get(user = user)
        if token.key != user_token.key:
            return Response(status=401)
        else:
            account_id = request.data["account_id"]
            routine_id = request.data["routine_id"]

            routine = Routine.objects.get(account_id = account_id, routine_id = routine_id)
            routine.delete()
            
            #response
            response = OrderedDict()            
                
            response["data"] = OrderedDict()
            response["data"]["routine_id"] = routine_id 

            response["message"] = OrderedDict()
            response["message"]["msg"] = " ."
            response["message"]["status"] = "ROUTINE_DELETE_OK"

            json.dumps(response, ensure_ascii=False, indent="\t")
        
            return Response(response)