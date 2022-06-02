from rest_framework.request import Request
from rest_framework.response import Response
from blood_bank.serializers import UserSerializer
from blood_bank.models import User
from rest_framework.views import APIView


class Signup(APIView):
    def post(self, request: Request):
        self.register_new_user(request.data)
        return Response({'msg': 'New user registered'})

    def register_new_user(self, request_data):
        serializer = UserSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
