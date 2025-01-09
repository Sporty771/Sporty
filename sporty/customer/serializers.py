from rest_framework import serializers
from customer.models import CustomUser  # Import CustomUser model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password is write-only for security
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser  # Specify the CustomUser model
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'profile_picture', 'password']

    def create(self, validated_data):
        # Extract password from the data
        password = validated_data.pop('password')
        # Create the user object with other fields
        user = CustomUser.objects.create_user(**validated_data)
        # Set hashed password
        user.set_password(password)
        # Save user
        user.save()
        return user
