from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    """Custom user manager for user model"""

    def create_user(self, email, password=None, phone=None, **extra_fields):
        """Create and return a regular user with an email, password, and optional phone."""
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        if phone:
            extra_fields['phone'] = phone  # Explicitly set phone if passed

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, phone=None, **extra_fields):
        """Create and return a superuser with email, password, and optional phone."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, phone=phone, **extra_fields)


class User(AbstractUser):
    """Custom user model to login with email and password"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    phone = PhoneNumberField(unique=True, region='IN')  # 'IN' for India (optional)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    username = None
    
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
class Permission(models.Model):
    """Model representing an individual permission that can be assigned to a role (e.g. create_test_series)"""
    code = models.CharField(max_length=100, unique=True)  # e.g. "create_test_series"
    name = models.CharField(max_length=255)  # Human-readable label

    def __str__(self):
        return self.name
    
class Role(models.Model):
    """Model representing a role (e.g. Admin, Tutor, Student) with a set of permissions"""
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    def __str__(self):
        return self.name

class UserRole(models.Model):
    """Model mapping users to roles. A user can have multiple roles."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'role')  # Prevent duplicate user-role assignments

    def __str__(self):
        return f"{self.user.email} → {self.role.name}"
