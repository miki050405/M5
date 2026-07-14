from celery import shared_task
from time import sleep
from django.conf import settings
from django.core.mail import send_mail
from users.models import CustomUser
from product.models import Review, Product

@shared_task
def new_review_email(review_id):
    review = Review.objects.get(id = review_id)
    send_mail(
        "Вам оставили новый отзыв",
        f" Продукт: {review.product}\n Отзыв: {review.text}",
        settings.EMAIL_HOST_USER,
        [review.product.owner.email],
        fail_silently=False,
    )
    return "OK"

@shared_task
def product_status():
    products = Product.objects.all()
    for product in products:
        avg = product.average_score
        if product.reviews.count() == 0:
            product.status = "Нет оценок"
        elif avg < 2:
            product.status = "Плохой"
        elif avg < 3.5:
            product.status = "Средний"
        elif avg < 4.5:
            product.status = "Хороший"
        else:
            product.status = "Отличный"
        product.save()
    return "Статусы товаров обновлены"

@shared_task
def count_reviews(product_id):
    product = Product.objects.get(id=product_id)
    count = product.reviews.count()
    result = f"У продукта {product.title} теперь {count} отзывов"
    print(result)
    return result
