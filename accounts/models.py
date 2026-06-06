from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils import timezone

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    email = models.EmailField(unique=True)

    is_verified = models.BooleanField(default=False)

    roles = models.ManyToManyField(
        Role,
        related_name="users",
        blank=True
    )
    
    reference_selfie = models.ImageField(upload_to="selfies/", null=True, blank=True)
    face_encoding = models.JSONField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']   #required internally

    def __str__(self):
        return self.email

class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)