from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login 
# authenticate: 사용자 인증을 담당(사용자명과 비밀번호가 정확한지 검증), login: 로그인 담당(사용자 세션 생성)
from django.shortcuts import render, redirect
from users.forms import UserForm

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('users:login')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})