from django.db import models
from django.contrib.auth.models import AbstractUser

import random

class ShopOwner(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, default='default_username')
    password = models.CharField(max_length=128, default='default_password')
    email = models.EmailField(unique=True, null=True)  # Keep the email field, but ensure it's used correctly
    is_email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    shop_name = models.CharField(max_length=255)
    address = models.TextField()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='shopowner_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='shopowner_permissions_set',
        blank=True
    )

    # Override the USERNAME_FIELD to use email for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'shop_name']  # You can add other fields to REQUIRED_FIELDS

    def __str__(self):
        return self.username

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

class Product(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # Upload image for product
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name