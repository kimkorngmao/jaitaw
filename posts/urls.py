from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name="all-post-list"),
    path('create/', PostCreateAPIView.as_view(), name="create-post"),
    path('read/<str:code>/', PostDetailAPIView.as_view(), name="read-post"),
    path('update/<str:code>/', PostUpdateAPIView.as_view(), name="update-post"),
    path('delete/<str:code>/', PostDeleteAPIView.as_view(), name="delete-post"),
    path('like/<str:code>/', PostLikeAPIView.as_view(), name="like-post"),
    path('save/<str:code>/', PostSaveAPIView.as_view(), name="save-post"),
    path('liked/', LikedPostAPIListView.as_view(), name="saved-post-list"),
    path('saved/', SavedPostAPIListView.as_view(), name="saved-post-list"),
]