from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='media/images/', blank=True, null=True)
    is_verify = models.BooleanField(default=False)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} Followed {self.following.username}"