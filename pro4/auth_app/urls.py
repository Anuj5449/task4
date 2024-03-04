from django.urls import path
from .views import fetchData,manageUser,useraccountActivate,user_creat

urlpatterns = [
    path('create/',user_creat),
    path('fetch/',fetchData),
    path('details/<int:pk>/',manageUser),
    path('activate/<uid>/<>token/',useraccountActivate, name='activate')
]
