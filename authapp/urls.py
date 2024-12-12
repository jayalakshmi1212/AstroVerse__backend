from django.urls import path
from .views import SignupView, LoginView,VerifyOTPView,LogoutView,ForgotPasswordView,ResetPasswordView,TutorSignupView,TutorVerifyOTPView,AdminLoginView,UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/',VerifyOTPView.as_view(), name='verify-otp'),
    path('logout/', LogoutView.as_view(), name='logout'),
     path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('api/reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),

    path('signup/tutor/', TutorSignupView.as_view(), name='tutor-signup'),
    path('tutor/verify-otp/', TutorVerifyOTPView.as_view(), name='tutor-verify-otp'),
     path('adminlogin/', AdminLoginView.as_view(), name='login'),
     
     path('profile/', UserProfileView.as_view(), name='user-profile'),
]
