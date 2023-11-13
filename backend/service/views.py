from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .models import User
import jwt

from django.contrib.auth import authenticate, get_user_model
from base.settings import SECRET_KEY
from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.hashers import check_password


class SignupAPIView(APIView):
    def post(self, request):
        serializer = SingupSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            #jwt token 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message":"register success",
                    "token":{
                        "access": access_token, 
                        "refresh": refresh_token,
                    },
                },
                status= status.HTTP_200_OK,
            )
            #cookie에 넣어주기
            res.set_cookie("access", access_token, httponly= True)
            res.set_cookie("refresh", refresh_token, httponly= True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    #user 정보 확인
    def get(self, request):
        try:
            #access token decode -> id 추출 = user 식별
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk = pk)
            serializer = UserSerializer(instance = user)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except(jwt.exceptions.ExpiredSignatureError):
            #token 만료 시 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenObtainPairSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                serializer = UserSerializer(instance = user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            return jwt.exceptions.InvalidTokenError
        except(jwt.exceptions.InvalidTokenError):
            #사용 불가 토큰인 경우
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    #로그인
    def post(self, request):
        id = request.data['id']
        user = User.objects.filter(id = id).first()

        #user 존재 X
        if user is None:
            return Response(
                {'message': "id Not exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user) #refresh token 생성
            refresh_token = str(token) #token 문자열화
            access_token = str(token.access_token)

            user.is_active = True
            user.save()

            x_fowarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

            if x_fowarded_for:
                ip = x_fowarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')


            res = Response(
                {
                    "user": serializer.data,
                    "ip": ip,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status = status.HTTP_200_OK,
            )

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly= True)
            return res
        else:
            return Response(
                {"message": "login failed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def delete(self, request):
        update_user = User.objects.get(email = request.data['id'])
        update_user.is_active = False
        update_user.save()

        #cookie에 저장된 token 삭제 -> logout 처리
        res = Response({
            "message": "Log out success"
        }, status= status.HTTP_202_ACCEPTED)
        res.delete_cookie('refresh')
        return res
    

# def detail(request, mywork_id):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip_list = x_forwarded_for.split(',')
#         client_ip = ip_list[0].strip()
#     else:
#         client_ip = request.META.get('REMOTE_ADDR')
#     context = { 'client_ip': client_ip,}
#     return render(request, 'mywork/detail.html',context)
# Create your views here.
