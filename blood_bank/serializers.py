from rest_framework import serializers

from blood_bank.models import MyUser
from django.contrib.auth import login, authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'name', 'email', 'cpf', 'password' ]
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password')

    def validate(self, data):
        """
            Verifica se existem usuarios com email e senha mandados
        """

                # if 'django' not in value.lower():
                # raise serializers.ValidationError("Blog post is not about Django")
    
        return data