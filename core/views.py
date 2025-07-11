from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = serializer.get_tokens(user)
        return Response({"user": serializer.data, "tokens": tokens}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    """View for user login using generics."""
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user_serializer = UserSerializer(user)
            return Response({
                "user": user_serializer.data,
                "tokens": UserSerializer.get_tokens(user)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)