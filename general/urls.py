from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name="home"),
    path('documentaion/accounts/', Account, name="account"),
    path('documentaion/posts/', Post, name="post"),
    path('documentaion/comments/', Comment, name="comment"),
    path('documentaion/notification/', Notification, name="notification"),
    path('documentaion/tag/', Tag, name="tag"),
]