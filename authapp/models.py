from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import timedelta
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='user'):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        return self.create_user(username, email, password, role='admin')

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('tutor', 'Tutor'),
    )
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=False)  # Initially False to prevent login until OTP verification
    is_staff = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)  # Store OTP directly in the user model
    otp_generated_at = models.DateTimeField(null=True, blank=True)  # Timestamp for OTP generation
    document_tutor=models.CharField(max_length=255,blank=True,null=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def is_otp_expired(self):
        if self.otp_generated_at:
            return self.otp_generated_at + timedelta(minutes=5) < timezone.now()
        return True  # If OTP is not generated, consider it expired


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.URLField(max_length=500, blank=True, null=True)  # Cloudinary image URL
    qualification = models.CharField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return f"{self.user.username}'s Profile"