from django.shortcuts import render
from blood_bank.serializers import UserSerializer
from blood_bank.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class Signup(APIView):
    def post(self, request):
        return Response('hello world')