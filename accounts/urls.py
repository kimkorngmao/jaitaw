from django.urls import path
from .views import *

# Create your urls here.

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login-view'),
    path('register/', RegisterAPIView.as_view(), name='register-view'),

    path('follow/<str:username>/', FollowUserAPIView.as_view(), name='follow-user'),
    path('profile/update/', EditProfileAPIView.as_view(), name='update-profile'),
    path('password/change/', ChangePasswordAPIView.as_view(), name='password-change'),

    path('me/', CurrentUserAPIView.as_view(), name='current-user-view'),
    path('following/', FollowingUserAPIListView.as_view(), name='following-users-list'),
    path('follower/', FollowerUserAPIListView.as_view(), name='follower-users-list'),
    path('<str:username>/', UserProfileDetailAPIView.as_view(), name='user-detail'),
]