from socket import create_server
from django.shortcuts import render
from blood_bank.serializers import SignupFormSerializer, LoginFormSerializer
from blood_bank.models import MyUser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login(request):
    """
     login no sistema usando email e password
    """
    if request.method == 'POST':
        serializer = LoginFormSerializer(data=request.data)

        if serializer.is_valid():
            email = request.data.get('email')            
            user = MyUser.objects.filter(email=email).first()
  
            token = Token.objects.get(user=user)
            return Response({'token': token.key }) 
        else:
            return Response(serializer._errors)

@api_view(['POST'])
def signup(request):
    """
    signup no sistema usando email e password
    """
    if request.method == 'POST':
        serializer = SignupFormSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key }) 
        else:
            return Response(serializer._errors)

    