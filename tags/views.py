from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from posts.models import Post
from posts.serializers import PostSerializer

# Create your views here.

class PostsByTagAPIListView(APIView):
    def get(self, request, tag_name, format=None):
        try:
            tag = Tag.objects.get(name__iexact=tag_name.lower())
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

        post_tags = PostTag.objects.filter(tag=tag)
        posts_with_tag = [post_tag.post for post_tag in post_tags]

        serializer = PostSerializer(posts_with_tag, many=True, context={'request': request})
        return Response({"posts" : serializer.data}, status=status.HTTP_200_OK)
