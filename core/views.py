from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, VerifyOTPSerializer, SendOTPSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth import get_user_model, authenticate
from utils.send_otp import send_otp_email
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

User = get_user_model()

@extend_schema(tags=["Auth"])
class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    Handles creation of a new user, validates input,
    and returns user data with authentication tokens.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create method to include JWT tokens in response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Get tokens using the instance method
        tokens = serializer.get_tokens(user)

        # Return user data using the serializer
        user_data = self.get_serializer(user).data

        return Response({
            "success": True,
            "message": "Registration successful",
            "data": {
                "user": user_data,
                "tokens": tokens,
            }
        }, status=status.HTTP_201_CREATED)

@extend_schema(tags=["Auth"])
class LoginView(generics.GenericAPIView):
    """
    API view for user login.

    This view handles user authentication by validating provided credentials.
    Upon successful authentication and verification of the user's account status
    (`is_verified` is True), it returns the user data along with authentication tokens.

    If the credentials are invalid or the user's account is not verified,
    appropriate error messages are returned.
    """
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        """
        Handles the login process.

        Validates the credentials, authenticates the user, and returns user data
        and authentication tokens if the credentials are correct and the user is verified.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        
        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if not user.is_verified:
                return Response({
                    "success": False,
                    "error": "Account not verified. Please verify your email before logging in."
                }, status=status.HTTP_403_FORBIDDEN)

            user_serializer = UserSerializer(user)
            return Response({
                "success": True,
                "message": "Login successful",
                "data": {
                    "user": user_serializer.data,
                    "tokens": UserSerializer().get_tokens(user)
                }
            }, status=status.HTTP_200_OK)
        
        # Return an error response if authentication fails
        return Response({
            "success": False,
            "error": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(tags=["Auth"])
class VerifyOTPView(generics.CreateAPIView):
    """
    API view to verify the OTP sent to the user's email.

    Marks the user's account as verified upon successful OTP validation.
    """
    serializer_class = VerifyOTPSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests for OTP verification.

        Validates the OTP, verifies the user account, and deletes the OTP.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data["otp"]
        otp.is_verified = True
        otp.save()

        return Response({
            "success": True,
            "message": "OTP verified",
        }, status=status.HTTP_200_OK)

@extend_schema(tags=["Auth"])     
class SendOTPView(generics.CreateAPIView):
    """
    API view to send an OTP to the user.

    POST  /send-otp/
    Body: { "email": "<email>" }

    Sends an OTP that is valid for 10 minutes.
    """
    serializer_class = SendOTPSerializer
    permission_classes = [permissions.AllowAny]
    # throttle_scope = "resend_otp"                         # optional DRF throttle

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests to resend OTP.

        Validates the email and sends a new OTP.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()          # actually sends the OTP

        return Response({
            "success": True,
            "message": "An OTP has been sent to your email."
        },status=status.HTTP_201_CREATED
        )

@extend_schema(tags=["Auth"])
class ForgotPasswordView(generics.CreateAPIView):
    """
    POST /forgot-password/

    Request a password reset link.
    """
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "Password reset link has been sent to your email."
        }, status=status.HTTP_200_OK)

@extend_schema(tags=["Auth"])
class ResetPasswordView(generics.CreateAPIView):
    """
    POST /reset-password/

    Confirm and reset password using uid and token.
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "Your password has been reset successfully."
        }, status=status.HTTP_200_OK)
        
@extend_schema_view(
    post=extend_schema(tags=["Token"])
)
class TokenObtainPairViewWithSchema(TokenObtainPairView):
    pass

@extend_schema_view(
    post=extend_schema(tags=["Token"])
)
class TokenRefreshViewWithSchema(TokenRefreshView):
    pass