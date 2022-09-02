from tokenize import blank_re
from typing_extensions import Required
from rest_framework import serializers
from blood_bank.models import MyUser
import json
from blood_bank.models import age_of_user

class LoginFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password')
    
    def validate_email(self, value):
        user = MyUser.objects.filter(email=value).first()
        
        if  value == '' or  value == None:
            raise serializers.ValidationError({"email": "Por favor preencha este campo com um e-mail valido."})
        elif user == None:
            raise serializers.ValidationError({"email": "Não existe usuário com este email."})

        return value
    
    def validate(self, data):
        user = MyUser.objects.filter(email=data['email']).first()
        if data['password'] == '' or data['password'] == None:
            raise serializers.ValidationError({"password": "Por favor preencha este campo com uma senha valida."})
        elif user == None or user.check_password(data['password']) == False:
            raise serializers.ValidationError({"password": "Senha invalida."})
        return data

class SignupFormSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'birth_date', 'password', 'confirm_password'] 

    def validate_username(self, value):
        if  value == '' or  value == None:
            raise serializers.ValidationError({"username": "Por favor preencha este campo com um nome de usuário valido."})
        elif MyUser.objects.filter(username=value).first():
            raise serializers.ValidationError({"username": "Já existe um usuário com este email."})

        return value
       
    def validate_email(self, value):
        if  value == '' or  value == None:
            raise serializers.ValidationError({"email": "Por favor preencha este campo com um e-mail valido."})
        elif MyUser.objects.filter(email=value).first():
            raise serializers.ValidationError({"email": "Já existe usuário com este email."})

        return value
    
    def validate_birth_date(self, value):
        if  value == '' or  value == None:
            raise serializers.ValidationError({"birth_date": "Por favor preencha este campo com uma data de nascimento valida."})
        elif age_of_user(value) < 16 :
            raise serializers.ValidationError({"birth_date": "Menores de 16 anos não podem doar sangue."})

        return value
    
    def validate(self, data):
        if  data["password"] == '' or  data["password"] == None:
            raise serializers.ValidationError({"password": "Por favor preencha este campo com uma senha valida."})
        
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Estas duas senhas não combinam."})
        
        if data['confirm_password'] == '' or data['confirm_password'] == None:
            raise serializers.ValidationError({"password": "Por favor preencha este campo com a senha que você escolheu."})
            
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return super().create(validated_data)

    
