from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'timestamp')  # Fields to display in the list view
    search_fields = ('sender__username', 'recipient__username', 'content')  # Add search functionality
    list_filter = ('timestamp',)  # Optionally filter by timestamp

# Register the Message model with the custom admin class
admin.site.register(Message, MessageAdmin)
