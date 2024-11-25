from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import UserSerializer, UserSignupSerializer,TutorSignupSerializer,TutorSerializer
from django.utils import timezone
from datetime import timedelta
import random
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode



####################################################### signup ###########################################################


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

            # Redirect the user to the OTP verification page
            otp_verification_url = reverse('tutor-verify-otp')  # You can change this to whatever URL you want
            return Response({
                "message": "OTP sent to your email. Please verify to complete signup.",
                "redirect_to": otp_verification_url  # Return the URL for redirection
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
############otp

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

##############################################Login################################################

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
    
###########Logout   
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


#####################forgot password
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Construct the password reset URL
            reset_url =f"http://localhost:5173/reset-password/{uid}/{token}/"

            # Send the email with the reset URL
            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n{reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
from rest_framework.permissions import AllowAny

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users

    def get(self, request, uidb64, token):
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_id)
            token_generator = PasswordResetTokenGenerator()

            # Verify if the token is valid
            if token_generator.check_token(user, token):
                return Response({"message": "Token is valid."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"error": "Invalid user."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, uidb64, token):
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_id)
            token_generator = PasswordResetTokenGenerator()

            # Verify if the token is valid
            if not token_generator.check_token(user, token):
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()

            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_404_NOT_FOUND)


#################################################################################################################
class TutorSignupView(APIView):
    def post(self, request):
        serializer = TutorSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate OTP
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.is_active = False  # Make tutor inactive until OTP verification
            user.otp_generated_at = timezone.now()  # Store the OTP generation time
            user.save()

            # Send OTP to the tutor's email
            send_mail(
                'Your OTP Code',
                f'Your OTP for verification is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            print(otp)
            # Redirect the tutor to the OTP verification page
            otp_verification_url = reverse('tutor-verify-otp')  # Replace with your actual verification URL name
            return Response({
                "message": "OTP sent to your email. Please verify to complete signup.",
                "redirect_to": otp_verification_url  # Frontend can use this to navigate
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TutorVerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email)

            # Check if OTP exists
            if user.otp is None:
                return Response({"detail": "OTP not sent or expired. Please request a new OTP."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if OTP is expired (5 minutes expiration)
            otp_expiry_time = user.otp_generated_at + timedelta(minutes=5)
            if timezone.now() > otp_expiry_time:
                user.otp = None  # Clear expired OTP
                user.save()
                return Response({"detail": "OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)

            # Verify the OTP
            if user.otp == otp:  # Convert OTP to integer for comparison
                user.is_active = True  # Activate the tutor account
                user.otp = None  # Clear OTP
                user.save()

                # Generate JWT tokens for the tutor
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                return Response({
                    'refresh': str(refresh),
                    'access': str(access),
                    'user': TutorSerializer(user).data,  # Serialize the tutor details
                    "message": "OTP verified successfully. Welcome!"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"detail": "Tutor not found"}, status=status.HTTP_404_NOT_FOUND)



from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

@method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for the class-based view
class AdminLoginView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            user = authenticate(request, email=email, password=password)
            if user is not None:
                if not user.is_active:
                    return JsonResponse({'error': 'Account not activated. Verify OTP first.'}, status=401)
                if not user.is_superuser:
                    return JsonResponse({'error': 'Only superusers are allowed to log in'}, status=403)
                return JsonResponse({'message': 'Login successful', 'user': {'id': user.id, 'email': user.email, 'role': user.role}})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
