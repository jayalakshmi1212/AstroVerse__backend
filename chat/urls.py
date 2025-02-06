from django.urls import path
from . import views
from .views import ChatStudentsView


urlpatterns = [
     path('api/chat-students/',ChatStudentsView.as_view(), name='chat_students'),
    
]
