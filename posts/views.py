import re
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import PostSerializer
from tags.models import Tag, PostTag
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        content = request.data.get('content')
        tags = [tag[1:] for tag in re.findall(r' #\w+', content)] # Remove "#"

        serializer = PostSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            instance = serializer.save()
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                PostTag.objects.create(post=instance, tag=tag)
            return Response({ "created_post": serializer.data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomPagination(PageNumberPagination):
    page_size = 10  # Set the number of posts per page
    page_size_query_param = 'size'
    max_page_size = 1000  # Set the maximum number of posts per page

class PostListView(APIView):
    def get(self, request, format=None):
        paginator = CustomPagination()
        posts = Post.objects.filter(status='public')
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response({"posts": serializer.data})
    
class PostDetailAPIView(APIView):
    def get(self, request, code, format=None):
        try:
            post = Post.objects.get(code=code, status="public")
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, context={'request':request})
        return Response({ "post": serializer.data }, status=status.HTTP_200_OK)

class PostUpdateAPIView(APIView):
    def get_post(self, code):
        try:
            return Post.objects.get(code=code)
        except Post.DoesNotExist:
            return None

    def put(self, request, code, format=None):
        content = request.data.get('content')
        tags = re.findall(r'#\w+', content)
        post = self.get_post(code)
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        if post.author.username != request.user.username:
            return Response({"error": "You have no permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                PostTag.objects.create(post=instance, tag=tag)

            return Response({"message": "Post updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDeleteAPIView(APIView):
    def get_post(self, code):
        try:
            return Post.objects.get(code=code)
        except Post.DoesNotExist:
            return None

    def delete(self, request, code, format=None):
        post = self.get_post(code)
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        if post.author.username != request.user.username:
            return Response({"error": "You have no permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, code):
        post = get_object_or_404(Post, code=code)
        user = request.user
        like_post = PostLike.objects.filter(user=user, post=post)
        if like_post.exists():
            like_post.delete()
            message = f"You have unlike {post.title}."
        else:
            PostLike.objects.create(user=user, post=post)
            message = f"You are now like {post.title}."
        return Response({"message": message}, status=status.HTTP_200_OK)

class PostSaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, code):
        post = get_object_or_404(Post, code=code)
        user = request.user
        save_post = PostSave.objects.filter(user=user, post=post)
        if save_post.exists():
            save_post.delete()
            message = f"You have unsave {post.title}."
        else:
            PostSave.objects.create(user=user, post=post)
            message = f"You are now save {post.title}."
        return Response({"message": message}, status=status.HTTP_200_OK)

class LikedPostAPIListView(APIView):
    def get(self, request):
        user = request.user
        article = Post.objects.filter(postlike__user_id=user.id)
        serializer = PostSerializer(article, many=True, context={'request':request})
        return Response({'posts':serializer.data})

class SavedPostAPIListView(APIView):
    def get(self, request):
        user = request.user
        article = Post.objects.filter(postsave__user_id=user.id)
        serializer = PostSerializer(article, many=True, context={'request':request})
        return Response({'posts':serializer.data})