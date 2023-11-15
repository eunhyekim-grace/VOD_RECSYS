from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from .models import User, VODInfo, UserLog
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
        update_user = User.objects.get(id = request.data['id'])
        update_user.is_active = False
        update_user.save()

        #cookie에 저장된 token 삭제 -> logout 처리
        res = Response({
            "message": "Log out success"
        }, status= status.HTTP_202_ACCEPTED)
        res.delete_cookie('refresh')
        return res

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import operator

user_log_data = UserLog.objects.all().values()
vod_info_data = VODInfo.objects.all().values()
user_log = pd.DataFrame(user_log_data)
vod_info = pd.DataFrame(vod_info_data)

score_matrix = user_log.pivot_table(index='subsr', columns='vod_id_id', values='use_tms')
score_matrix = score_matrix.fillna(0)


def similar_users(user_id, score_matrix, k=5):
    # 현재 user_id에 대한 데이터프레임 준비
    user = score_matrix[score_matrix.index == user_id]
    # 나머지 user들에 대한 정보
    other_user = score_matrix[score_matrix.index != user_id]
    # 대상 user와 나머지 user들과의 유사도 계산
    sim = cosine_similarity(user, other_user)[0].tolist()
    # 나머지 user들에 대한 목록 생성
    other_users_list = other_user.index.tolist()
    # 인덱스/유사도로 이루어진 딕셔너리 생성
    user_sim = dict(zip(other_users_list, sim))
    # 딕셔너리 정렬
    user_sim_sorted = sorted(user_sim.items(), key=operator.itemgetter(1))
    # 가장 높은 유사도 k개 정렬
    top_users_sim = user_sim_sorted[:k]
    users = [i[0] for i in top_users_sim]
    return users

def recommend_vod(user_index, similar_user_indices, matrix, items=10):
    # 유저와 비슷한 유저 가져오기
    sim_users = matrix[matrix.index.isin(similar_user_indices)]
    # 비슷한 유저 평균 계산
    sim_users = sim_users.mean(axis=0)
    sim_users_df = pd.DataFrame(sim_users, columns=['user_similarity'])
    # 현재 사용자의 벡터 가져오기
    user_df = matrix[matrix.index == user_index]
    # 현재 사용자의 평가 데이터 정렬
    user_df_transposed = user_df.transpose()
    user_df_transposed.columns = ['time'] 
    # 미시청 vod 목록리스트 만들기
    unseen_vod = user_df_transposed[user_df_transposed['time']==0].index.tolist()
    # 미시청 vod 필터링
    sim_users_df_filtered = sim_users_df[sim_users_df.index.isin(unseen_vod)]
    # 평균값을 기준으로 내림차순 정렬
    sim_users_df_ordered = sim_users_df_filtered.sort_values(by='user_similarity', ascending=False)
    # 상위 n개 값 가져오기
    top_n_vod = sim_users_df_ordered.head(items)
    top_n_vod_indices = top_n_vod.index.tolist()
    # vod_info 데이터프레임에서 top_n값 찾기
    vod_information = vod_info[vod_info['vod_id'].isin(top_n_vod_indices)]
    # 추천작품 리스트
    results = set(vod_information['title'].tolist())
    return results

class ProfileView(APIView):
    def get(self, request):
        try:
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])

            pk = payload.get('user_id')
            user = get_object_or_404(User, pk = pk)
            serializer = UserSerializer(instance= user)

            if serializer.data.get('is_active', None):
                user_id = serializer.data.get('id', None)
                result = recommend_vod(user_id, similar_users(user_id, score_matrix), score_matrix)
                return Response(result)
                #return Response(serializer.data.get('id', None), status=status.HTTP_200_OK)
            else:
                return Response({"message": "please log in first"}, status= status.HTTP_403_FORBIDDEN)
           
            # return render(request, 'profile.html', {'rec': serializer.data})
        except(jwt.exceptions.InvalidSignatureError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status = 400)

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

