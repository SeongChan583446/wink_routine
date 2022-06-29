from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Routine)
admin.site.register(models.RoutineResult)
admin.site.register(models.RoutineDay)