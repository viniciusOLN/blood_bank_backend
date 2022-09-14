from tokenize import blank_re
from rest_framework import serializers
from blood_bank.models import MyUser
import json
from blood_bank.models import age_of_user
from rest_framework.validators import UniqueValidator
import re
from django import forms

class LoginFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password')
    
    def validate_email(self, value):
        user = MyUser.objects.filter(email=value).first()
        
        if  value == '' or  value == None:
            raise serializers.ValidationError("Por favor preencha este campo com um e-mail valido.")
        elif user == None:
            raise serializers.ValidationError("Não existe usuário com este email.")

        return value
    
    def validate(self, data):
        user = MyUser.objects.filter(email=data['email']).first()
        if data['password'] == '' or data['password'] == None:
            raise serializers.ValidationError("Por favor preencha este campo com uma senha valida.")
        elif user == None or user.check_password(data['password']) == False:
            raise serializers.ValidationError("Senha invalida.")
        return data



class SignupFormSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[
        UniqueValidator(
            queryset=MyUser.objects.all(),
            message="Já existe um usuário com este nome.",
        )]
        ,allow_blank=True
    )
    confirm_password = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'birth_date', 'password', 'confirm_password'] 
        extra_kwargs = {
            "email": {"allow_blank": True},
            "birth_date": {"allow_null": True},
            "password": {"allow_null": True, 'allow_blank': True},
        }

    
    def validate_username(self, value):
        if  value == '' or  value == None:
            raise serializers.ValidationError({"username": "Por favor preencha este campo com um nome de usuário valido."})

        return value
       
    def validate_email(self, value):
        if  value == '' or  value == None:
            raise serializers.ValidationError({"email": "Por favor preencha este campo com um e-mail valido."})
        elif MyUser.objects.filter(email=value).first():
            raise serializers.ValidationError({"email": "Já existe usuário com este email."})

        return value
    
    def to_internal_value(self, data):
        if data['birth_date'] == '':
            data['birth_date'] = None
        if not re.match(r'\d{4}\-\d{2}\-\d{2}', str(data['birth_date'])):
            data['birth_date'] = None

        return super(SignupFormSerializer, self).to_internal_value(data)

    def validate_birth_date(self, value):
        if  value == '' or  value == None:
            raise serializers.ValidationError({"birth_date": "Por favor preencha este campo com uma data de nascimento valida."})
        elif age_of_user(value) < 16 :
            raise serializers.ValidationError({"birth_date": "Menores de 16 anos não podem doar sangue."})

        return value
    
    def validate(self, data):
        errors={}
        if not data.get('password'):
            errors['password'] = "Por favor preencha este campo com uma senha valida."
        if not data.get('confirm_password'):
            errors['confirm_password'] = "Por favor preencha este campo com a mesma senha anterior."
        elif data.get('password') != data.get('confirm_password'):
            errors['confirm_password'] = "Estas duas senhas não combinam."
        
        if errors:
            raise forms.ValidationError(errors)

        return data
        
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return super().create(validated_data)

    
