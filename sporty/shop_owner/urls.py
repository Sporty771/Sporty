from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopOwnerViewSet, SendOTPView, VerifyEmailView, ProductViewSet

# Router for viewsets
router = DefaultRouter()
router.register('shopowner', ShopOwnerViewSet, basename='shopowner-viewset')  # Updated basename
router.register('products', ProductViewSet, basename='product')

# Add paths for APIView classes
urlpatterns = [
    path('', include(router.urls)),
    path('shop-otp/', SendOTPView.as_view(), name='shop-otp'),  # For sending OTP
    path('shop-verify-otp/', VerifyEmailView.as_view(), name='shop-verify-otp'),  # For verifying OTP
]
