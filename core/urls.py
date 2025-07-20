from django.urls import path
from .views import RegisterView, LoginView, VerifyOTPView, SendOTPView, ForgotPasswordView, ResetPasswordView, TokenObtainPairViewWithSchema, TokenRefreshViewWithSchema

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("send-otp/", SendOTPView.as_view(), name="send_otp"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path('token/', TokenObtainPairViewWithSchema.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshViewWithSchema.as_view(), name='token_refresh'),
]
