from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title description price category'.split()

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text product'.split()

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    product_id = serializers.IntegerField()
    stars = serializers.IntegerField(min_value=1, max_value=5, default=5)

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')
        return product_id

class ProductListReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title description price category review_text average_score'.split()

class CategoriesProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name products_count'.split()