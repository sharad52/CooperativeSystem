from os import name
from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('',loginPage,name="login"),
    path('register/',registerPage,name="register"),
    path('logout/',logoutUser,name="logout"),
    path('update-profile/',UpdateProfile,name="ProfileUpdate"),
    path('view-profile/<int:pk>/',ViewProfile,name='ViewProfile'),
]

