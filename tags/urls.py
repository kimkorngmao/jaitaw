from django.urls import path
from .views import *

urlpatterns = [
    path('posts/<str:tag_name>/', PostsByTagAPIListView.as_view(), name='posts-by-tag'),
]