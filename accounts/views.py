from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from .customcreate import CreateUserForm
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import TokenSerializer
from rest_framework.permissions import IsAuthenticated


#회원가입--------------------------------------------------------------------------------


class UsersignupAPIView(APIView):
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

       
# #로그인--------------------------------------------------------------------------------
class UserloginAPIView(APIView):
    def post(self,request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
    
            User = get_user_model()
            refresh = RefreshToken.for_user(User)
            
            serializer = TokenSerializer({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
            

            
    #   구현: 성공적인 로그인 시 토큰을 발급하고, 실패 시 적절한 에러 메시지를 반환.      
            
    # 프로필 조회-------------------------------------------------------------
    
class UserprofileAPIView(APIView):
        
    # permission_classes = [IsAuthenticated]
        
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
# - **조건**: 로그인 상태 필요.
# - **검증**: 로그인 한 사용자만 프로필 조회 가능
# - **구현**: 로그인한 사용자의 정보를 JSON 형태로 반환.