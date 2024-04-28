from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerialzer
from .models import Notification
from rest_framework.response import Response

# Create your views here.

class NotificationAPIListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user)
        serializer = NotificationSerialzer(notifications, many=True, context={'request':request})
        return Response({'notifications' : serializer.data})

class NotificationBadgeAPIView(APIView):
    def get(self, request):
        notifications_count = 0
        if request.user.is_authenticated:
            notifications_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'total_count' : notifications_count})
    
class MarkAllNotificationsAsReadAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(recipient=request.user, is_read=False)
        queryset.update(is_read=True)
        return Response({'message': 'All notifications have been marked as read.'})