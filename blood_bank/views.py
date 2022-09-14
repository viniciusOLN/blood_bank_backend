from blood_bank.serializers import SignupFormSerializer, LoginFormSerializer
from blood_bank.models import MyUser
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
     login no sistema usando email e password
    """
    if request.method == 'POST':
        serializer = LoginFormSerializer(data=request.data)

        if serializer.is_valid():
            email = request.data.get('email')            
            user = MyUser.objects.filter(email=email).first()
  
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Usuário logado com sucesso.',
                'token': token.key
                }) 
        else:
            return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    signup no sistema usando email e password
    """
    if request.method == 'POST':
        serializer = SignupFormSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()

            token, created = Token.objects.get_or_create(user=user).key
            return Response({
                'message': 'Usuário registrado com sucesso.',
                'token': token.key 
                }) 
        else:
            return Response(serializer._errors)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()

    response = {
        'message': 'Usuário Deslogado com sucesso.'
    }

    return Response(response)