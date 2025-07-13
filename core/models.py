from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import random
from django.utils import timezone
from datetime import timedelta

class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.

    Provides methods to create regular users and superusers using email as the unique identifier.
    """

    def create_user(self, email, password=None, phone=None, **extra_fields):
        """
        Create and return a regular user with an email, password, and optional phone number.

        :param email: Email address of the user
        :param password: Raw password for the user
        :param phone: Phone number (optional)
        :param extra_fields: Additional user fields
        :return: User instance
        """
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        if phone:
            extra_fields['phone'] = phone

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, phone=None, **extra_fields):
        """
        Create and return a superuser with email, password, and optional phone number.

        :param email: Email address of the superuser
        :param password: Raw password
        :param phone: Phone number (optional)
        :param extra_fields: Additional fields to set (e.g., is_staff, is_superuser)
        :return: Superuser instance
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, phone=phone, **extra_fields)


class User(AbstractUser):
    """
    Custom user model that uses email for authentication instead of username.

    Additional fields:
        - phone: Unique phone number
        - is_verified: Boolean indicating whether the user has verified their email
    """

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    phone = PhoneNumberField(unique=True, region='IN')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    username = None

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Permission(models.Model):
    """
    Model representing an individual permission that can be assigned to a role.

    Example: "create_test_series", "delete_user", etc.
    """

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Role(models.Model):
    """
    Model representing a role (e.g., Admin, Tutor, Student).

    Each role is associated with a set of permissions.
    """

    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    def __str__(self):
        return self.name


class UserRole(models.Model):
    """
    Model mapping users to roles.

    A user can have multiple roles, and each mapping is timestamped.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'role')  # Prevent duplicate assignments

    def __str__(self):
        return f"{self.user.email} → {self.role.name}"


class OTP(models.Model):
    """
    Model to store a One-Time Password (OTP) for a user.

    Each user is associated with a single OTP instance via a one-to-one relationship.
    The OTP is a 6-digit numeric code, and it expires 10 minutes after creation.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def generate_otp(self):
        """
        Generate a new 6-digit OTP for the user.

        Updates the `otp_code` with a random number and resets `created_at` timestamp.
        """
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.created_at = timezone.now()
        self.save()

    def is_expired(self):
        """
        Check whether the OTP has expired.

        :return: True if more than 10 minutes have passed since creation, else False
        :rtype: bool
        """
        return timezone.now() > self.created_at + timedelta(minutes=10)
