
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, AuthSerializer, ConfirmationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode, CustomUser
import secrets
from rest_framework.exceptions import ValidationError
from django.db import transaction
from rest_framework.generics import CreateAPIView

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
            ConfirmCode.objects.create(
                user = user,
                code = code
            )

        return Response(status=status.HTTP_201_CREATED,
                        data={'user_id': user.id, 'code':code})

class ConfirmationApiView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = ConfirmationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        try:
            conf_code = ConfirmCode.objects.get(code = code)
        except ConfirmCode.DoesNotExist:
            raise ValidationError('Код неверный. Повторите попытку!')
        
        user = conf_code.user
        user.is_active = True
        user.save()
        conf_code.delete()
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

