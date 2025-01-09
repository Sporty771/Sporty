from rest_framework import serializers
from .models import ShopOwner,Product
from shop_owner.models import ShopOwner


class ShopOwnerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should be write-only
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = ShopOwner
        fields = ['id','username','shop_name', 'password', 'address', 'phone_number', 'email']

    def create(self, validated_data):
        # Extract fields from validated_data
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')  # Extract username

        # Create the ShopOwner instance
        shop_owner = ShopOwner.objects.create_user(
            username=username,
            email=email,
            password=password,
            **validated_data
        )
        shop_owner.set_password(password)
        shop_owner.save()

        return shop_owner


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'shop_owner', 'name', 'description', 'price', 'stock', 'image', 'created_at', 'updated_at']