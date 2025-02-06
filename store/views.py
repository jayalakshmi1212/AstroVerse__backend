from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .storeSerializer import CategorySerializer
from rest_framework.permissions import IsAuthenticated
from authapp.models import User
from authapp.serializers import UserSerializer,TutorSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

class CategoryListCreateView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryUpdateDeleteView(APIView):
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)

from rest_framework.permissions import AllowAny
from django.http import JsonResponse

class UserListView(APIView):
    def get(self, request):
        print('enterrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        print(request.user)  # Should show the authenticated user
        print(request.auth)  # Should show the token
        users = User.objects.all().values('id', 'username', 'email', 'is_active',)
        return Response({'users': list(users)}, status=status.HTTP_200_OK)

@api_view(['POST'])
def toggle_user_status(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.is_active = not user.is_active
        user.save()
        return Response({'message': 'User status updated successfully', 'is_active': user.is_active}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def get_courses(request):
    courses = Course.objects.all()
    serializer = CourseCreateSerializer(courses, many=True)
    return Response({'courses': serializer.data})

############################# tutor list ################################

@api_view(['GET'])
def list_tutors(request):
    tutors = User.objects.filter(role='tutor')  # Filter by role
    tutor_data = [
        {
            'id': tutor.id,
            'username': tutor.username,
            'email': tutor.email,
            'role': tutor.role,
            'is_active': tutor.is_active,  # Include is_active
             'document_tutor': tutor.document_tutor,  # Include document URL
            'approval_status': tutor.approval_status  # Include approval status
        }
        for tutor in tutors
    ]
    return Response({'tutors': tutor_data}, status=status.HTTP_200_OK)
@api_view(['POST'])
def update_tutor_approval_status(request, user_id):
    try:
        user = User.objects.get(pk=user_id, role='tutor')  # Ensure only tutors can be updated
        new_status = request.data.get('approval_status')
        if new_status not in ['approved', 'rejected']:
            return Response({'error': 'Invalid approval status'}, status=status.HTTP_400_BAD_REQUEST)

        user.approval_status = new_status
        user.is_active = (new_status == 'approved')  # Activate only if approved
        user.save()
        return Response({'message': 'Tutor approval status updated', 'approval_status': user.approval_status}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Tutor not found'}, status=status.HTTP_404_NOT_FOUND)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Lesson
from .storeSerializer import LessonSerializer, CourseDetailSerializer,CourseCreateSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

# class AddCourseView(APIView):
#     def post(self, request):
#         print('add course entered')
#         serializer = CourseCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddCourseView(APIView):
    def post(self, request):
        # Assuming the tutor's ID is passed as 'created_by' in the request data
        user_id = request.data.get('created_by')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Tutor not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the course
        course_data = {**request.data, 'created_by': user.id}
        serializer = CourseCreateSerializer(data=course_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CourseListView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseCreateSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseDetailView(APIView):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data)
    
    def put(self, request, pk):
        course = Course.objects.get(pk=pk)
        serializer = CourseDetailSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = Course.objects.get(pk=pk)
        course.delete()
        return Response({"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class AddLessonView(APIView):
    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TutorCourseListView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can view the courses

    def get(self, request):
        # Get the logged-in tutor's ID
        user = request.user

        # Filter courses by the tutor (created_by)
        courses = Course.objects.filter(created_by=user)

        # Serialize the courses data
        serializer = CourseCreateSerializer(courses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
from django.db.models import Count
    
class CourseListView(APIView):
    
    def get(self, request):
        courses = Course.objects.annotate(lesson_count=Count('lessons')).filter(lesson_count__gt=0)
        serializer = CourseCreateSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseDetailUser(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            serializer = CourseCreateSerializer(course)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
import razorpay
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


class InitiatePaymentAPIView(APIView):
    def post(self, request):
        amount = request.data.get("amount", 0)  # Amount in paise
        currency = "INR"
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            # Create an order
            order = client.order.create({"amount": amount, "currency": currency, "payment_capture": 1})
            return Response(order, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Enrollment, Course
from django.conf import settings

class ConfirmPaymentView(APIView):
    def post(self, request):
        user = request.user  # Assumes the user is authenticated
        payment_id = request.data.get("payment_id")
        course_id = request.data.get("course_id")

        if not payment_id or not course_id:
            return Response({"error": "Missing payment details"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
            Enrollment.objects.create(
                user=user,
                course=course,
                payment_id=payment_id
            )
            return Response({"message": "Enrollment successful"}, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EnrollmentStatusView(APIView):
    def get(self, request, course_id):
        user = request.user  # Assumes authentication middleware is in place
        try:
            is_enrolled = Enrollment.objects.filter(user=user, course_id=course_id).exists()
            return Response({"is_enrolled": is_enrolled}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
class CourseLessonsView(APIView):
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        lessons = course.lessons.all()  # Fetch all lessons related to this course
        lesson_serializer = LessonSerializer(lessons, many=True)
        print(lesson_serializer.data,'data of lesson')
        return Response(lesson_serializer.data)
    
    

from rest_framework import generics
from .models import Comment
from .storeSerializer import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None)  # Fetch top-level comments only
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        return Comment.objects.filter(lesson_id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_id')
        parent_id = self.request.data.get('parent')

        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
                if parent.lesson_id != lesson_id:
                    raise ValidationError("Parent comment does not belong to this lesson.")
            except Comment.DoesNotExist:
                raise ValidationError("Parent comment does not exist.")

            serializer.save(user=self.request.user, lesson_id=lesson_id, parent=parent)
        else:
            serializer.save(user=self.request.user, lesson_id=lesson_id)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Review, Course
from store.storeSerializer import ReviewSerializer
from rest_framework import status
from rest_framework.generics import ListAPIView

class SubmitReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        user = request.user
        course = Course.objects.get(id=course_id)

        # Check if user has already reviewed this course
        if Review.objects.filter(user=user, course=course).exists():
            return Response({"error": "You have already reviewed this course."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new review
        data = request.data
        review = Review.objects.create(
            user=user,
            course=course,
            review_text=data.get('review_text'),
            rating=data.get('rating')
        )
        return Response({"message": "Review submitted successfully!"}, status=status.HTTP_201_CREATED)

class CourseReviewsView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        try:
            # Ensure the course exists
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        return Review.objects.filter(course__id=course_id)
    
class TutorCourseReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'tutor':
            return Response({'detail': 'You are not authorized to view tutor reviews.'}, status=403)

        tutor = request.user  # Get the logged-in tutor (User)
        courses = Course.objects.filter(created_by=tutor)  # Filter courses by the tutor
        reviews = Review.objects.filter(course__in=courses)  # Get reviews for these courses
        serializer = ReviewSerializer(reviews, many=True)
        return Response({'count': len(reviews), 'results': serializer.data})
