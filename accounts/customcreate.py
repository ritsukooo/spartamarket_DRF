
from django.contrib.auth.forms import UserCreationForm
# 장고의 유저 관련 내장 모델
from .models import User
from django import forms

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()  
    username = forms.CharField(max_length=150)
    name = forms.CharField(max_length=15, label="name")
    nickname = forms.CharField(max_length=30, label="Nickname")
    birthday = forms.DateField(label="Birthday")
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender")

    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2', 'name', 'nickname', 'birthday', 'gender']
        
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['nickname'].required = True
        self.fields['birthday'].required = True
        self.fields['name'].required = True


      
#  - **조건**: username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능
# - **검증**: username과 이메일은 유일해야 하며, 이메일 중복 검증(선택 기능).
# - **구현**: 데이터 검증 후 저장  
     
