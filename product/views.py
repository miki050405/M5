from .models import Category, Product, Review
from .serializers import (CategoryListSerializer, CategoryDetailSerializer, 
                          ProductListSerializer, ProductDetailSerializer, ReviewListSerializer, ReviewDetailSerializer, 
                          ProductListReviewSerializer, CategoriesProductsSerializer, 
                          CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return self.serializer_class

class ProductDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductValidateSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductDetailSerializer
        return self.serializer_class

class ReviewListCreateApiView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

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
