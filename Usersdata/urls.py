from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('users', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('users/<int:id>', UserView.as_view(), ),
]
