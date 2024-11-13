from django.urls import path
from .views import SignupView, LoginView,VerifyOTPView,LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/',VerifyOTPView.as_view(), name='verify-otp'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
