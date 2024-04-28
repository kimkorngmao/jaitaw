from django.urls import path
from .views import *

urlpatterns = [
    path('inbox/', NotificationAPIListView.as_view(), name="inbox-list"),
    path('badge/', NotificationBadgeAPIView.as_view(), name="inbox-count"),
    path('mark/all/', MarkAllNotificationsAsReadAPIView.as_view(), name="mark-all-as-read"),
]