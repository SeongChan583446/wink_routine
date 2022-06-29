from django.urls import path

from . import views
from . import account, routine

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',account.SignupView.as_view()),
    path('login/',account.LoginView.as_view()),
    path('createroutine/',routine.CreateRoutineView.as_view()),
    path('inquirelist/',routine.InquireRoutineListView.as_view()),
    path('inquire/',routine.InquireRoutineView.as_view()),
    path('update/',routine.UpdateRoutineView.as_view()),
    path('delete/',routine.DeleteRoutineView.as_view()),
]