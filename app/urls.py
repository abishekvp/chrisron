from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
    path('index',main,name="main"),
    path('login',user_login,name="login"),
    path('logout',user_logout,name="logout"),
    path('register',user_register,name="register"),
    path('e9877y43uygf734teg9746t3bufy497t',show,name="view"),
]