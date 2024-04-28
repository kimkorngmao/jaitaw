from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateCommentAPIView.as_view(), name="create-comment"),
    path('read/<int:id>/', CommentDetailAPIView.as_view(), name="read-comment"),
    path('update/<int:id>/', CommentUpdateAPIView.as_view(), name="upate-comment"),
    path('delete/<int:id>/', CommentDeleteAPIView.as_view(), name="delete-comment"),
    path('like/<int:id>/', CommentLikeAPIView.as_view(), name="like-comment"),
    path('post/<str:post_code>/', CommentsByPostAPIListView.as_view(), name="all-comment-by-post-list"),
]

"""
POST http://127.0.0.1:8000/comments/create/
Content-Type: application/json
"""