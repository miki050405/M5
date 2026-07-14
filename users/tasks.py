from celery import shared_task
from time import sleep
from django.conf import settings
from django.core.mail import send_mail
from users.models import CustomUser

@shared_task
def add(x, y):
    print("Отчет...")
    sleep(20)
    print("Завершено")
    return x + y

@shared_task
def send_email(code, email):
    send_mail(
        "Приветствуем на нашей платформе",
        f"Вот твой код для регистрации: {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return "OK"

@shared_task
def delete_unactive_users():
    deleted = CustomUser.objects.filter(is_active=False).delete()
    return f"Удалены: {deleted}"
