from .models import User
from rest_framework import serializers
# from .models import *

class SingupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
       id = validated_data.get('id')
       user = User(
            id = id
        )
       user.save()
       return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        return User(**validated_data)