from django.db import models
from authapp.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    tag_line = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="courses", on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    about = models.TextField()
    thumbnail = models.URLField()  # Store Cloudinary URL
    created_by = models.ForeignKey(User, related_name="created_courses", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_url = models.URLField()  # For video file URL (use a storage service)
    description = models.TextField()
    tutor = models.ForeignKey(User, related_name='tutored_lessons', on_delete=models.SET_NULL, null=True, blank=True)  # Tutor field


    def __str__(self):
        return self.title
class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    
    
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="enrollments", on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255, null=True, blank=True)  # Razorpay Payment ID
    is_paid = models.BooleanField(default=False)  # To track if payment is complete
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:30]}"

    class Meta:
        ordering = ['-created_at']

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # Ensure one review per user per course

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"