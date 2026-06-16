from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, AuthSerializer, ConfirmationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode
import secrets
from rest_framework.exceptions import ValidationError
from django.db import transaction

@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False
        )
        
        code = str(secrets.randbelow(900000) + 100000)
        ConfirmCode.objects.create(
            user = user,
            code = code
        )

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id, 'code':code})

@api_view(['POST'])
def confirmation_api_view(request):
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


@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


