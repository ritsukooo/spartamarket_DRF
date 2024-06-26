from . import views
from django.contrib import admin
from django.urls import include, path
from .views import (
    UsersignupAPIView, UserloginAPIView, UserprofileAPIView,
    UserwithdrawAPIView,UserlogoutAPIView
)


app_name = "accounts"
urlpatterns = [
    path("", UsersignupAPIView.as_view(), name="signup"),  # 회원가입
    path("login/", UserloginAPIView.as_view(), name="login"),  # 로그인
    path("withdraw/", UserwithdrawAPIView.as_view()),  # 회원탈퇴
    path("profile/<str:username>/",
         UserprofileAPIView.as_view(), name="profile"),  # 프로필
    path("logout/", UserlogoutAPIView.as_view(), name="logout"), #로그아웃

]
