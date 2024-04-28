from rest_framework import serializers
from accounts.serializers import UserSerializer
from comments.models import Comment
from .models import Post, PostLike, PostSave

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    is_save = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Post
        
        fields = ['code', 'target', 'title', 'content', 'author', 'created', 'updated', 'like_count', 'is_like', 'is_save', 'status', 'views', 'comment_count']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)
    
    def get_target(self, obj):
        return f"/post/{obj.code}"
    
    def get_comment_count(self, obj):
        return Comment.objects.filter(post=obj).count()
    
    def get_like_count(self, obj):
        return PostLike.objects.filter(post=obj).count()
    
    def get_is_like(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_authenticated:
                return PostLike.objects.filter(user=user, post=obj).exists()
        return False

    def get_is_save(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_authenticated:
                return PostSave.objects.filter(user=user, post=obj).exists()
        return False
    
    def get_updated(self, obj):
        # check if request user is the author of the post
        request = self.context['request']
        if request:
            if request.user.username == obj.author.username:
                return obj.updated
        return None