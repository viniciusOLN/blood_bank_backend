from tokenize import blank_re
from typing_extensions import Required
from rest_framework import serializers
from blood_bank.models import MyUser
import json


class LoginFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password')
    
    def validate_email(self, value):
        user = MyUser.objects.filter(email=value).first()
        
        if  value == '' or  value == None:
            raise serializers.ValidationError({"email": "Por favor preencha o campo com um e-mail valido."})
        elif user == None:
            raise serializers.ValidationError({"email": "Não existe usuário com este email."})

        return value
    
    def validate_password(self, value):
        user = MyUser.objects.filter(email=value).first()
        if value == '' or value == None:
            raise serializers.ValidationError({"password": "Por favor preencha o campo com uma senha valida."})
        elif user == None or user.check_password(value) == False:
            raise serializers.ValidationError({"password": "Senha invalida."})
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'name', 'email', 'cpf', 'password' ]
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user

