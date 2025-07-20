from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.serializerfields import PhoneNumberField as PhoneNumberSerializerField
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .models import OTP
from utils.send_email_ import send_email
from utils.templates import reset_password_email_template , otp_email_template
from django.conf import settings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user in the system.

    Handles validation for unique email and phone number,
    and creates a new user with a hashed password.
    """

    phone = PhoneNumberSerializerField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone", "password"]

    def get_tokens(self, user):
        """
        Generate access and refresh tokens for a given user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def validate_email(self, value):
        """
        Ensure the provided email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value):
        """
        Ensure the provided phone number is unique.
        """
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone already exists.")
        return value

    def validate(self, attrs):
        """
        Validate that the email has a verified OTP entry.
        """
        email = attrs.get("email")
        otp_instance = OTP.objects.filter(email=email).first()

        if not otp_instance or not otp_instance.is_verified:
            raise serializers.ValidationError("Email is not verified yet.")

        return attrs

    def create(self, validated_data):
        """
        Create a new user with a securely hashed password.
        """
        user = User.objects.create_user(**validated_data)
        user.is_verified = True
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging in a user.

    Validates email and password fields.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})


class VerifyOTPSerializer(serializers.Serializer):
    """
    Serializer for verifying a user's OTP.

    Accepts an email and 6-digit OTP, validates them, and checks expiration.
    """

    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        """
        Validate OTP and email combination.

        :param attrs: Input data
        :return: Validated data with user and otp objects
        :raises ValidationError: If validation fails at any step
        """
        email = attrs.get("email")
        otp_input = attrs.get("otp")

        try:
            otp = OTP.objects.get(email=email)
        except OTP.DoesNotExist:
            raise serializers.ValidationError({"otp": "No user found with this email"})

        if otp.is_expired():
            otp.delete()
            raise serializers.ValidationError({"otp": "OTP expired, please request a new one."})

        if otp.otp_code != otp_input:
            raise serializers.ValidationError({"otp": "Invalid OTP."})

        attrs["otp"] = otp
        return attrs


class SendOTPSerializer(serializers.Serializer):
    """
    Serializer to send OTP to a user.

    Accepts an email address and validates if the account is unverified.
    """

    email = serializers.EmailField()

    def validate_email(self, email):
        """
        Checks if the email exists in the OTP model and if it is already verified.
        """
        otp_instance = OTP.objects.filter(email=email).first()
        if otp_instance and otp_instance.is_verified:
            raise serializers.ValidationError("Account already verified.")
        return email

    def create(self, validated_data):
        email = validated_data['email']

        # Delete any existing OTP for this email to enforce uniqueness
        OTP.objects.filter(email=email).delete()

        # Create a new OTP instance
        otp_instance = OTP(email=email)
        otp_instance.generate_otp()  # This saves the instance
        
        # Send OTP Email
        send_email(
            subject="Your OTP Code",
            message=None,
            html_message=otp_email_template(otp_instance.otp_code),
            recipient_list=[email]
        )
        return otp_instance

class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer to initiate password reset by sending a reset link to the user's email.

    :param email: Registered email
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # Send the reset link via email
        send_email(
            subject="Reset your password",
            # message=f"Click the link to reset your password:\n{reset_link}",
            message=None,
            html_message=reset_password_email_template(user.first_name, user.last_name, reset_link),
            recipient_list=[user.email]
        )
        return user


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer to reset the password via reset link with UID and token.

    :param uid: Base64-encoded user ID
    :param token: Reset token
    :param new_password: New password to set
    """
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True) # min_length=6 

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uid"]))
            self.user = User.objects.get(id=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({"uid": "Invalid or expired reset link."})

        if not PasswordResetTokenGenerator().check_token(self.user, attrs["token"]):
            raise serializers.ValidationError({"token": "Reset token is invalid or expired."})

        return attrs

    def save(self):
        password = self.validated_data["new_password"]
        self.user.set_password(password)
        self.user.save()
        return self.user