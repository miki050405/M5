from django.db import models
from users.models import CustomUser
from common.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    @property
    def products_count(self):
        return len(self.products.all())
    
class Product(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    @property
    def review_text(self):
        return [i.text for i in self.reviews.all()]

    @property
    def average_score(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([i.stars for i in reviews])/len(reviews) 
        else:
            return 0
    
class Review(BaseModel):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    stars = models.IntegerField(choices=((i, i) for i in range(1, 6)),default=5)
    
    def __str__(self):
        return self.text[:15]
    
