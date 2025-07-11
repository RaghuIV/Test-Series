from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view handles the creation of a new user, validates the input data,
    and returns the serialized user data along with authentication tokens.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Overrides the 'create' method to handle user registration.

        Validates the request data, creates a user, and generates authentication tokens.
        Returns the user data along with tokens in the response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = serializer.get_tokens(user)
        return Response({
            "user": serializer.data,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    API view for user login.

    This view validates the user's credentials and returns the user data and tokens
    upon successful authentication.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Handles the login process.

        Validates the credentials, authenticates the user, and returns user data
        and authentication tokens if the credentials are correct.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        
        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            user_serializer = UserSerializer(user)
            return Response({
                "user": user_serializer.data,
                "tokens": UserSerializer.get_tokens(user)
            }, status=status.HTTP_200_OK)
        
        # Return an error response if authentication fails
        return Response({
            "error": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)
