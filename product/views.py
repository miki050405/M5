from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (CategoryListSerializer, CategoryDetailSerializer, 
                          ProductListSerializer, ProductDetailSerializer, ReviewListSerializer, ReviewDetailSerializer, 
                          ProductListReviewSerializer, CategoriesProductsSerializer, 
                          CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer)



@api_view(['GET','PUT','DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerializer(category, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=CategoryDetailSerializer(category).data
        )


@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategoriesProductsSerializer(categories, many=True).data
        return Response(
            data=data,  
        )
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        
        name = serializer.validated_data.get('name')
        category = Category.objects.create(
            name = name,
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data=CategoryDetailSerializer(category).data
        )

@api_view(['GET','POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductListSerializer(products, many = True).data
        return Response(
            data = data,
        )
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')

        product = Product.objects.create(
            title = title,
            description = description,
            price = price,
            category_id = category_id,
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductDetailSerializer(product).data
        )

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request,id):
    try:
        product = Product.objects.get(id = id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many = False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductDetailSerializer(product).data
        )

@api_view(['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewListSerializer(reviews, many = True).data
        return Response(
            data = data,
        )
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text')
        product_id = serializer.validated_data.get('product_id')
        stars = serializer.validated_data.get('stars')

        review = Review.objects.create(
            text = text,
            product_id = product_id,
            stars = stars,
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data = ReviewDetailSerializer(review).data
        )

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request,id):
    try:
        review = Review.objects.get(id = id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many = False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        
        review.text = serializer.validated_data.get('text')
        review.product_id = serializer.validated_data.get('product_id')
        review.stars = serializer.validated_data.get('stars')
        review.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewDetailSerializer(review).data
        )

@api_view(['GET'])
def product_list_review_api_view(request):
    products = Product.objects.all()
    data = ProductListReviewSerializer(products, many = True).data
    return Response(
        data = data,
    )
