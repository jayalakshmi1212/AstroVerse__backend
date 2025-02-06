from rest_framework import serializers
from .models import Category,Course,Lesson,User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

from .models import Course, Lesson

from django.contrib.auth import get_user_model
User = get_user_model()
class CourseCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="name"  # Match the category name instead of ID
    )

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_url','tutor']

class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

from rest_framework import serializers
from .models import Comment

class ReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Adjust based on how `user` should be represented
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'lesson', 'content', 'parent', 'replies', 'created_at']


from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user = serializers.CharField(source='user.username')
    course_name = serializers.CharField(source='course.title')

    class Meta:
        model = Review
        fields = ['user', 'review_text', 'rating', 'created_at','course_name']
