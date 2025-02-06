from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message,User
from authapp.serializers import UserSerializer

class ChatStudentsView(APIView):
    
    def get(self, request):
        # Get all users who have sent a message
        students = User.objects.filter(id__in=Message.objects.values('sender_id').distinct())
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)

