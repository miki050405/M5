from .models import Category, Product, Review
from .serializers import (CategoryListSerializer, CategoryDetailSerializer, 
                          ProductListSerializer, ProductDetailSerializer, ReviewListSerializer, ReviewDetailSerializer, 
                          ProductListReviewSerializer, CategoriesProductsSerializer, 
                          CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from common.permissions import IsAuth, IsAnon, CanEditWithIn15Minutes, IsModerator
from common.validators import validate_age
from rest_framework.response import Response
from rest_framework import status
from product.tasks import new_review_email, count_reviews

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'id'

class CategoryListCreateApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesProductsSerializer

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return CategoryDetailSerializer
        return self.serializer_class

class ProductListCreateApiView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductValidateSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            permission_classes = [IsModerator]
        else:
            permission_classes = [IsAuth | IsAnon]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        validate_age(self.request)
        return serializer.save(owner_id = self.request.auth.get("user_id"))

class ProductDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductValidateSerializer
    lookup_field = 'id'
    permission_classes = [IsAnon | (CanEditWithIn15Minutes & IsAuth) | IsModerator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductDetailSerializer
        return self.serializer_class
    

class ReviewListCreateApiView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

    def perform_create(self, serializer):
        review = serializer.save()
        count_reviews.delay(review.product_id)
        new_review_email.delay(review.id)
    
    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return ReviewValidateSerializer
        return self.serializer_class

class ReviewDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT']:
            return ReviewValidateSerializer
        return self.serializer_class

class ProductListReviewApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListReviewSerializer
