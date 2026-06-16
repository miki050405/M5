from django.urls import path
from product import views

urlpatterns = [
    path('categories/', views.CategoryListCreateApiView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('products/', views.ProductListCreateApiView.as_view()),
    path('products/<int:id>/', views.ProductDetailApiView.as_view()),
    path('reviews/', views.ReviewListCreateApiView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailApiView.as_view()),
    path('products/reviews/', views.ProductListReviewApiView.as_view()),
]