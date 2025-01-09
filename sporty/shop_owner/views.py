from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shop_owner.models import ShopOwner,Product
from rest_framework import viewsets
from shop_owner.models import ShopOwner
from shop_owner.serializers import ShopOwnerSerializer,ProductSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from .utils import send_otp_email  # Assuming this function is defined in a utils.py file

class ShopOwnerViewSet(viewsets.ModelViewSet):
    queryset = ShopOwner.objects.all()  # Corrected 'objects' here
    serializer_class = ShopOwnerSerializer
    permission_classes = [AllowAny]  # Corrected 'permission_classes' here, not 'permission_class'

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            # Corrected the model name to 'ShopOwner'
            shop_owner = ShopOwner.objects.get(email=email)
            shop_owner.generate_otp()  # Use 'shop_owner' instead of 'user'
            send_otp_email(shop_owner.email, shop_owner.otp)  # Make sure 'send_otp_email' is correctly defined
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        except ShopOwner.DoesNotExist:  # Corrected model name to 'ShopOwner'
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            # Corrected the model name to 'ShopOwner'
            shop_owner = ShopOwner.objects.get(email=email, otp=otp)
            shop_owner.is_email_verified = True  # Corrected the attribute access
            shop_owner.otp = None  # Clear OTP after verification
            shop_owner.save()  # Save changes
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        except ShopOwner.DoesNotExist:  # Corrected model name to 'ShopOwner'
            return Response({"error": "Invalid email or OTP."}, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Adjust permissions as necessary

    def perform_create(self, serializer):
        # Automatically associate the product with the logged-in shop owner
        shop_owner = self.request.user  # Use the logged-in user directly
        serializer.save(shop_owner=shop_owner)

    def get_queryset(self):
        # Return only the products belonging to the logged-in shop owner
        shop_owner = self.request.user  # Use the logged-in user directly
        return Product.objects.filter(shop_owner=shop_owner)



