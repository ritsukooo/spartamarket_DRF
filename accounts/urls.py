from . import views
from django.contrib import admin
from django.urls import include, path
from .views import UsersignupAPIView,UserloginAPIView,UserprofileAPIView





app_name = "accounts"
urlpatterns = [
    path("", UsersignupAPIView.as_view(), name="signup"),
    path("login/", UserloginAPIView.as_view(), name="login"),
    path("<str:username>/", UserprofileAPIView.as_view(), name="profile")

      
]