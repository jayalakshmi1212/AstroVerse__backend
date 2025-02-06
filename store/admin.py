from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Course, Lesson,Enrollment,Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')  # Columns to display in the list view
    search_fields = ('name', 'description')  # Add a search bar for these fields
    ordering = ('created_at',)  # Default ordering

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'price')  # Columns to display
    search_fields = ('title', 'tag_line')  # Add a search bar for title and tag_line
    list_filter = ('difficulty', 'category')  # Add filters for difficulty and category
    ordering = ('title',)  # Default ordering

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')  # Columns to display
    search_fields = ('title', 'content')  # Add a search bar for title and content
    list_filter = ('course',)  # Add filter for courses
from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'payment_id', 'enrolled_at')  # Use 'enrolled_at' instead of 'created_at'
    search_fields = ('user__username', 'course__title', 'payment_id')  # Adjust field names to match your model
    list_filter = ('course', 'enrolled_at')  # Use 'enrolled_at' instead of 'created_at'
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'content_snippet', 'created_at')
    search_fields = ('user__username', 'lesson__title', 'content')
    list_filter = ('created_at', 'lesson')
    ordering = ('-created_at',)

    def content_snippet(self, obj):
        return obj.content[:50]  # Display first 50 characters of the content
    content_snippet.short_description = 'Comment Content'
