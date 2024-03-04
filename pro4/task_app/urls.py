from django.urls import path
from .views import create_task, details_api

urlpatterns = [
    path('task/', create_task),
    path('details/<int:pk>/',details_api)
]