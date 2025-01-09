from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SendOTPView, VerifyEmailView, ProductViewSet


# Initialize the router
router = DefaultRouter()
router.register('user', UserViewSet, basename='task-viewset')

# Define urlpatterns
urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email')
]

# Include router-generated URLs
urlpatterns += router.urls