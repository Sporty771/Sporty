from rest_framework import viewsets
from customer.models import CustomUser  # Use the CustomUser model
from customer.serializers import UserSerializer  # Import the serializer
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import send_otp_email
from shop_owner.models import Product  # Ensure this import is added
from shop_owner.serializers import ProductSerializer  # Import the serializer for Product

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
#define a funtion for veryfyimg email through otp

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            user.generate_otp()
            send_otp_email(user.email, user.otp)
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = CustomUser.objects.get(email=email, otp=otp)
            user.is_email_verified = True
            user.otp = None
            user.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid email or OTP."}, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Customers can only view products, not modify them

    def get_queryset(self):
        return Product.objects.all()  # Customers can view all products from any shop owner