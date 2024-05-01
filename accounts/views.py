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
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate


# 회원가입--------------------------------------------------------------------------------


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
    def post(self, request):

        user = authenticate(**request.data)
        if not user:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        # user가 있는경우
        refresh = RefreshToken.for_user(user)
        serializer = TokenSerializer({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

        return Response(serializer.data)

    #   구현: 성공적인 로그인 시 토큰을 발급하고, 실패 시 적절한 에러 메시지를 반환.

    # 프로필 조회 및 회원탈퇴-------------------------------------------------------------


class UserprofileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):

        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# - **조건**: 로그인 상태 필요.
# - **검증**: 로그인 한 사용자만 프로필 조회 가능
# - **구현**: 로그인한 사용자의 정보를 JSON 형태로 반환.


# 회원탈퇴--------------------------------------------------------------------------------

class UserwithdrawAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        password = request.data.get('password')

        if not password:
            return Response({'error': '비밀번호를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자가 입력한 비밀번호와 데이터베이스의 비밀번호 비교
        if not check_password(password, user.password):
            return Response({'error': '비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 로그아웃--------------------------------------------------------------------------------

class UserlogoutAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        
        token_string = request.data.get('access')
        token = RefreshToken(token_string)
        token.blacklist()
        return Response(status=status.HTTP_200_OK)       
        
        # 구현: 토큰 무효화 또는 다른 방법으로 로그아웃 처리 가능.
        
