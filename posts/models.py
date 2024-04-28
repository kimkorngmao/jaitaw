from django.db import models
from accounts.models import User
import random
import string

# Create your models here.

class PostManager(models.Manager):
    def published(self):
        return self.filter(status='public')

class Post(models.Model):
    STATUS_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('banned', 'Banned'),
    )
    code = models.CharField(max_length=11, unique=True, blank=True)
    title = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='public')
    views = models.PositiveIntegerField(default=0)

    objects = PostManager()

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate a random string of length 11
            while True:
                code = ''.join(random.choices(string.ascii_letters + string.digits, k=11))
                if not Post.objects.filter(code=code).exists():
                    break
            self.code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk} - {self.title}"

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"

class PostSave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'post')
    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"