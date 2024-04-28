from rest_framework import serializers
from .models import *
from accounts.serializers import UserSerializer
from posts.serializers import *
from django.shortcuts import get_object_or_404

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created', 'updated', 'author', 'like_count', 'is_like']
        partial = True

    def create(self, validated_data):
        request = self.context['request']
        if request.user.is_authenticated:  # Check that the user is authenticated
            post_code = request.data['post_code']
            post = get_object_or_404(Post, code=post_code)
            validated_data['post'] = post
            validated_data['author'] = request.user
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("You must be logged in to comment on a post.")

    def get_like_count(self,obj):
        return CommentLike.objects.filter(comment=obj).count()

    def get_is_like(self,obj):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_authenticated:
                return CommentLike.objects.filter(user=user, comment=obj).exists()
        return False