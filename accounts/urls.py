from . import views
from django.contrib import admin
from django.urls import include, path




app_name = "accounts"
urlpatterns = [
    path("", views.UsersignupAPIView.as_view(), name="signup"),
    path("login/", views.UserloginAPIView.as_view(), name="login"),
    # path("/<str:username> ", views..as_view(), name="profile"),
      
]