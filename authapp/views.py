from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import UserSerializer, UserSignupSerializer
from django.utils import timezone
from datetime import timedelta
import random
from rest_framework.permissions import IsAuthenticated


class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.is_active = False
            user.otp_generated_at = timezone.now()  # Store the time OTP was created
            user.save()

            # Send OTP to the user's email
            send_mail(
                'Your OTP Code',
                f'Your OTP for verification is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to your email. Please verify to complete signup."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email)

            # Check if OTP exists
            if user.otp is None:
                return Response({"detail": "OTP not sent or expired. Please request a new OTP."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if OTP is expired (5 minutes expiration time)
            otp_expiry_time = user.otp_generated_at + timedelta(minutes=5)
            print("Stored OTP:", type(user.otp))  # Debug
            
            if timezone.now() > otp_expiry_time:
                user.otp = None  # Clear expired OTP
                user.save()
                return Response({"detail": "OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)
            print("Stored OTP:", type(user.otp))  # Debug
            print("Provided OTP:", type(otp)) 
            print("OTPs Match:", user.otp == otp)
            print("OTPs Match:", user.otp == int(otp))
            # Check if OTP matches
            if user.otp == otp:
                user.is_active = True  # Mark user as active
                user.otp = None  # Clear OTP after verification
                user.save()

                # Generate JWT tokens for the user
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data,
                    "message": "OTP verified successfully. You are now logged in."
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user with email and password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if not user.is_active:
                return Response({"detail": "Account not activated. Please verify your OTP."}, status=status.HTTP_403_FORBIDDEN)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)