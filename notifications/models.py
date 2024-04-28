from django.db import models
from accounts.models import User, Follow
from posts.models import Post, PostLike
from comments.models import Comment

# Create your models here.

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('activity', 'Activity'),
        ('system', 'System'),
    )

    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default="activity")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent', blank=True, null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received')
    message = models.TextField()
    path = models.CharField(max_length=255,null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notifications_post', null=True, blank=True)
    post_like = models.ForeignKey(PostLike, on_delete=models.CASCADE, related_name='notifications_post_like', null=True, blank=True)
    post_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='notifications_post_comment', null=True, blank=True)
    user_follow = models.ForeignKey(Follow, on_delete=models.CASCADE, related_name='notifications_user_follow', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_hide = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.message