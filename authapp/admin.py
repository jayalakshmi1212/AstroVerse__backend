from django.contrib import admin
from .models import User,Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_active', 'is_staff')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'qualification', 'profile_image')  # Fields to show in the admin list view
    search_fields = ('user__username', 'phone_number', 'qualification')  # Fields to search by
