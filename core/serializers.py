from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.serializerfields import PhoneNumberField as PhoneNumberSerializerField
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration in the system"""
    
    phone = PhoneNumberSerializerField()
    
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def create(self, validated_data):
        """Create a new user with hashed password."""
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_phone(self, value):
        """Ensure phone is unique."""
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone already exists.")
        return value

class LoginSerializer(serializers.Serializer):
    """Serializer for User to login in the system"""
    email = serializers.EmailField()
    password = serializers.CharField()


