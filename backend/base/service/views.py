from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import User

import jwt
from django.contrib.auth import authenticate, get_user_model
from base.settings import SECRET_KEY
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

# class SignupAPIView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data = request.data)
#         if serializer.is_valid():
#             user = serializer.save()

#             #jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "message": "register successs",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )

#             #jwt token -> cookie 저장
#             res.set_cookie("access", access_token, httponly= True)
#             res.set_cookie("refresh", refresh_token, httponly= True)

#             return res
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# class AuthAPIView(APIView):
#     #user 정보 확인
#     def get(self, request):
#         try:
#             #access token을 decode해서 유저 id 추출 -> 유저 식별
#             access = request.COOKIES['access']
#             payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
#             pk = payload.get('user_id')
#             user = get_object_or_404(User, pk = pk)
#             serializer = UserSerializer(instance=user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         except(jwt.exceptions.ExpiredSignatureError):
#             #token 만료 시 토큰 갱신
#             data = {'refresh': request.COOKIES.get('refresh', None)}
#             serializer = TokenRefreshSerializer(data = data)
#             if serializer.is_valid(raise_exception=True):
#                 access = serializer.data.get('access', None)
#                 refresh = serializer.data.get('refresh', None)
#                 payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
#                 pk = payload.get('user_id')
#                 serializer = UserSerializer(instance=user)
#                 res = Response(serializer.data, status=status.HTTP_200_OK)
#                 res.set_cookie('access', access)
#                 res.set_cookie('refresh', refresh)
#                 return res
#             return jwt.exceptions.InvalidTokenError

#         except(jwt.exceptions.InvalidTokenError):
#             #사용 불가 토큰의 경우
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     #login
#     def post(self, request):
#         #user 인증
#         user = authenticate(
#             email = request.data.get('email'),
#             password = request.data.get("password")
#         )
#         #이미 있는 유저의 경우
#         if user is not None:
#             serializer = UserSerializer(user)
#             #jwt token 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "message": "login success",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             #jwt token -> cookie 저장
#             res.set_cookie('access', access_token, httponly=True)
#             res.set_cookie('refresh', refresh_token, httponly=True)
#             return res
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     #log out
#     def delete(self, request):
#         #cookie에 저장된 token 삭제 -> logout 처리
#         response = Response({
#             "message": "Log out success"
#         },
#         status= status.HTTP_202_ACCEPTED
#         )
#         response.delete_cookie('access')
#         response.delete_cookie('refresh')
#         return response

#회원 가입
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
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            #쿠키에 넣어주기...아직 어떤식으로 해야될지 모르겠는데 이렇게 설정만 우선 해주었다. 
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#log in
class LoginView(APIView):
    # user 정보 확인
    def get(self, request):
        try:
            #access token을 decode해서 유저 id 추출 -> 유저 식별
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk = pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except(jwt.exceptions.ExpiredSignatureError):
            #token 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            return jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            #사용 불가 토큰의 경우
            return Response(status=status.HTTP_400_BAD_REQUEST)


    #log in
    def post(self, request):

        # user = authenticate(
        #     email = request.data.get('email'),
        #     password = request.data.get('password')
        # )
        email = request.data['email']
        pw = request.data['password']

        user = User.objects.filter(email = email).first()

        #user 존재 X
        if user is None:
            return Response(
                {"message": "Email Not exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        #pw wrong
        if not check_password(pw, user.password):
            return Response(
                {"message": "Wrong Password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user) #refresh token 생성
            refresh_token = str(token) #token 문자열화
            access_token = str(token.access_token)

            user.is_active = True
            user.save()

            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            res.set_cookie("access",access_token, httponly= True) #post method로 login 했을때 생성된 token을 쿠키에 담아 전송
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(
                {"message":"login failed"},
                 status=status.HTTP_400_BAD_REQUEST)
    
    #logout
    def delete(self, request):
        update_user = User.objects.get(email = request.data['email'])
        update_user.is_active = False
        update_user.save()

        #cookie에 저장된 token 삭제 -> logout 처리
        res = Response({
            "message":"Log out success"
        }, status=status.HTTP_202_ACCEPTED)
        # res.delete_cookie('jwt')
        # res.delete_cookie('accesss')
        res.delete_cookie('refresh')
        return res
        
    
# class LogoutView(APIView):
#     def post(self, request):
#         # serializer = UserSerializer(user)
#         refresh_token = request.data['refresh']
#         token = RefreshToken(refresh_token)
#         token.blacklist()
#         res = Response(
#             {"message": "logout success"}, status=status.HTTP_200_OK
#         )
#         res.delete_cookie('jwt')
#         return res
#         #redirect('')
#         #return render(request, '#.html')

# def login_decorator(func):
#     def wrapper(self, request, *args, **kwargs):
#         try:
#             # access_token = request.headers.get('access', None)      
#             access_token = request.COOKIES['access']    
#             payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')  
#             user = User.objects.get(email=payload['email'])             
#             request.user = user                                                

#         except jwt.exceptions.DecodeError:
#             return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

#         except User.DoesNotExist:                                           
#             return JsonResponse({'message' : 'INVALID_USER'}, status=400)

#         return func(self, request, *args, **kwargs)

#     return wrapper
    

# class HomeView(APIView):
#     def post(self):
#         res = Response({
#             "you are already in"
#         }, status=status.HTTP_200_OK)
#         return res

class ProfileView(APIView):
    def get(self, request):
        try:
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            
            # user =User.objects.get(email = payload['email'])
            # user_id = user

            pk = payload.get('user_id')
            user = get_object_or_404(User, pk = pk)
            serializer = UserSerializer(instance= user)
            # user_id = serializer.data.get('subsr', None)
            
            # subsr = serializer.data.get('subsr', None)

            if serializer.data.get('is_active', None):
                 return Response(serializer.data.get('id', None), status=status.HTTP_200_OK)
            else:
                return Response({"message": "please log in first"}, status= status.HTTP_403_FORBIDDEN)
           
            
            # return render(request, 'profile.html', {'rec': serializer.data})
        except(jwt.exceptions.InvalidSignatureError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status = 400)
        # user_id = request.user.email
        # res = HttpResponse("<p> {{user_id}} </p>")
        # return res
        # return render(request, 'profile.html', {'recommendations':user_id})

from django.views import View

def basic(request):
  return render(request, 'basic.html')