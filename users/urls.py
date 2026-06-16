from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.RegistrationApiView.as_view()),
    path('authorization/', views.AuthorizationApiView.as_view()),
    path('confirmation/', views.ConfirmationApiView.as_view()),
]