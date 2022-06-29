from operator import mod
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Routine(models.Model):
    routine_id = models.AutoField(primary_key=True)
    account_id = models.IntegerField()
    title = models.CharField(max_length=20,default="")
    category = models.CharField(max_length=20)
    goal = models.CharField(max_length=20)
    is_alarm = models.BooleanField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add = True)
    modified_at = models.DateField(auto_now = True)

class RoutineResult(models.Model):
    routine_result_id = models.AutoField(primary_key=True)
    routine_id = models.ForeignKey(Routine, db_column='routine_id',on_delete=models.CASCADE)
    result = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add = True)
    modified_at = models.DateField(auto_now = True)

class RoutineDay(models.Model):
    day = models.CharField(max_length=20)
    routine_id = models.ForeignKey(Routine, db_column='routine_id',on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add = True)
    modified_at = models.DateField(auto_now = True)