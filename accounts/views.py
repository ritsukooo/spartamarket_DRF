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
from django.contrib.auth.hashers import check_password


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

    # 프로필 조회 및 회원탈퇴-------------------------------------------------------------


class UserprofileAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request, username):

        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        # user = request.user
        # serializer = UserSerializer(user)
        return Response(serializer.data)

# - **조건**: 로그인 상태 필요.
# - **검증**: 로그인 한 사용자만 프로필 조회 가능
# - **구현**: 로그인한 사용자의 정보를 JSON 형태로 반환.


# 회원탈퇴--------------------------------------------------------------------------------


class UserwithdrawAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def delete(self, request, users_pk):

        # password = request.data.get('password')

        # if not password:
        #     return Response({'error': '비밀번호를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자가 입력한 비밀번호와 데이터베이스의 비밀번호 비교
        # if not check_password(password, user.password):
        #     return Response({'error': '비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, users_pk=2)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# - **회원 탈퇴**
#     - **Endpoint**: **`/api/accounts`**
#     - **Method**: **`DELETE`**
#     - **조건**: 로그인 상태, 비밀번호 재입력 필요.
#     - **검증**: 입력된 비밀번호가 기존 비밀번호와 일치해야 함.
#     - **구현**: 비밀번호 확인 후 계정 삭제.
