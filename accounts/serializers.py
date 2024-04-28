from rest_framework import serializers
from .models import User, Follow
# Create your serializer here.

class UserSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    is_follow = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'bio', 'profile_image', 'following_count', 'follower_count', 'is_follow', 'is_verify']

    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_is_follow(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:  # Check authentication (optional)
            return Follow.objects.filter(follower=request.user, following=obj).exists()
        return False
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user == instance:
            return data
        else:
            del data['email']
            return data