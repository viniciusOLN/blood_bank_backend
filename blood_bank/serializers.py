from rest_framework import serializers

from blood_bank.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'cpf'
        ]

