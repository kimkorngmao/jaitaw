from rest_framework import serializers
from .models import Notification

class NotificationSerialzer(serializers.ModelSerializer):
    notification_from = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'notification_from', 'message', 'created', 'is_read', 'path', 'notification_type')
        
    def get_notification_from(self, obj):
        if obj.notification_type == "activity":
            if obj.author is not None:
                return obj.author.username
            else:
                return "Jaitaw"
        else:
            return "Jaitaw"