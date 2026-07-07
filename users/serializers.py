from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import ValidationError

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = serializers.CharField(max_length = 15,required=False)

    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError('User already exists!')
    
class ConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length = 6, min_length = 6)
