from socket import create_server
from django.shortcuts import render
from blood_bank.serializers import UserSerializer, LoginSerializer
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

class Login(APIView):
    """
        login com email e password
    """
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
            user = MyUser.objects.filter(email=email).first()
            if user != None and user.check_password(password) :           
                token = Token.objects.get(user=user)
                return Response({
                    'token': token.key,
                })
                # 'name': user.name,
                # 'email': user.email
            else:
               return JsonResponse("Email ou senha incorretos",safe=False)
        else:  
            return JsonResponse("Falha no login.",safe=False)


        
# class Exampleofauthenticationverificate(viewsets.ModelViewSet):
#     queryset = MyUser.objects.all()
#     serializer_class = UserSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated, ]
