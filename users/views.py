from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegisterSerializer, 
    AuthSerializer, 
    ConfirmationSerializer,
    CustomTokenObtainPairSerializer
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser
import secrets
from rest_framework.exceptions import ValidationError
from django.db import transaction
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegistrationApiView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        phone_number = serializer.validated_data.get('phone_number','')

        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                phone_number = phone_number,
                is_active=False
            )
            
            code = str(secrets.randbelow(900000) + 100000)
            cache.set(f"code:{user.id}", code, 300)

        return Response(status=status.HTTP_201_CREATED,
                        data={'user_id': user.id, 'code':code})

class ConfirmationApiView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = ConfirmationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        code = serializer.validated_data['code']

        conf_code = cache.get(f"code:{user_id}")
        if (conf_code is None) or (conf_code != code):
            raise ValidationError('Код неверный. Повторите попытку!')
        
        user = CustomUser.objects.get(id = user_id)
        cache.delete(f"code:{user_id}")
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)


class AuthorizationApiView(CreateAPIView):
    serializer_class = AuthSerializer
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)

