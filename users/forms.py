# 계정 생성시 사용할 UserForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

# django.contrib.auth.forms 모듈의 UserCreationForm 클래스 상속
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일") # email 속성 추가

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "nickname", "email")