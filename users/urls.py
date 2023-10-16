from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

# django.contrib.auth 앱의 LoginView 클래스를 활용 -> 별도의 views.py 파일 수정 필요 없음
app_name = 'users'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # 로그아웃 url 연결
    path('signup/', views.signup, name='signup')
]
