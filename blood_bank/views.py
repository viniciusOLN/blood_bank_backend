from blood_bank.serializers import *
from blood_bank.models import *
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

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
            user = serializer.save(commit=False)
            user.is_active = True
            user.set_password(user.password)
            user.save()

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Usuário registrado com sucesso.',
                'token': token.key, 
                'username': '', 
                'email': '', 
                'birth_date': '', 
                'password': '', 
                'confirm_password': '',
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

class CreatePerfil(APIView):
    """
        criar perfil e editar perdil de doador do sistema
    """
    def get_object(self, pk):
        try:
            return Donator.objects.get(pk=pk)
        except Donator.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        serializer = CreateEditDonatorSerializer(data=request.data)

        if serializer.is_valid():
            donator = serializer.save()
            donator.is_active = True
            donator.save()

            return Response({
                'message': 'Perfil criado com sucesso.',
                'perfil': serializer.data
            })
        else: 
            return Response({
                'message': 'Perfil não pode ser criado',
                'errors': serializer._errors
            })

    def put(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
