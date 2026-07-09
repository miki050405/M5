from rest_framework.exceptions import ValidationError
from datetime import  datetime
from django.utils import timezone

def validate_age(request):
    birthdate = request.auth.get("birthdate")
    if not birthdate:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт")
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    today = timezone.now()
    age = today.year - birthdate.year  - ((today.month, today.day)< (birthdate.month, birthdate.day))
    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт")
