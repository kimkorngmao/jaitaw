from django.db.models.signals import post_save,post_delete, pre_delete, pre_save, m2m_changed
from django.dispatch import receiver
from .models import Notification
from accounts.models import Follow, User
from posts.models import Post, PostLike
from comments.models import *

@receiver(post_save, sender=User)
def new_register_notification(sender, instance, created, **kwargs):
    if created:
        message = "Welcome to Jaitaw! Let's begin by customizing your profile now."
        Notification.objects.create(
            recipient=instance,
            message=message,
            path="/account/edit",
            notification_type="system"
        )

@receiver(post_save, sender=Follow)
def follow_user_notification(sender, instance, created, **kwargs):
    if created:
        recipient = instance.following
        follower = instance.follower
        message = f"{follower.full_name} (@{follower.username}) started following you."
        Notification.objects.create(
            author=follower,
            recipient=recipient,
            message=message,
            user_follow = instance,
            path=f"/{follower.username}"
        )

# Change this later
@receiver(post_save, sender=Post)
def new_post_notification(sender, instance, created, **kwargs):
    if created:
        authors = instance.author.followers.all()
        for author in authors:
            message = f"{author.following.full_name} (@{author.following.username}) posted a new post : {instance.title}."
            Notification.objects.create(
                recipient=author.follower,
                message=message,
                post = instance,
                path=f"/post/{instance.code}"
            )
    else:
        if instance.status == 'banned':
            message = f"Your post have been banned : {instance.title}."
            Notification.objects.create(
                recipient=instance.author,
                message=message,
                post = instance,
                path=f"/post/{instance.code}"
            )

@receiver(post_save, sender=Comment)
def new_comment_notification(sender, instance, created, **kwargs):
    if created:
        recipient = instance.post.author
        commentAuthor = instance.author
        message = f"{commentAuthor.full_name} (@{commentAuthor.username}) commented to your post : {instance.post.title}."
        if recipient != commentAuthor:
            Notification.objects.create(
                author=commentAuthor,
                recipient=recipient,
                message=message,
                post_comment = instance,
                path=f"/post/{instance.post.code}?comment={instance.id}"
            )

@receiver(post_save, sender=PostLike)
def like_post_notification(sender, instance, created, **kwargs):
    if created:
        recipient = instance.post.author
        liker = instance.user
        post = instance.post
        if recipient != liker:
            message = f"{liker.full_name} (@{liker.username}) liked to your post: {post.title}."
            Notification.objects.create(
                author=liker,
                recipient=recipient,
                message=message,
                post_like = instance,
                path=f"/post/{post.code}"
            )

@receiver(post_save, sender=CommentLike)
def comment_like_notification(sender, instance, created, **kwargs):
    if created:
        recipient = instance.comment.author
        liker = instance.user
        message = f"{liker.full_name} (@{liker.username}) started liked your comment."
        Notification.objects.create(
            author=liker,
            recipient=recipient,
            message=message,
            path=f"/{liker.username}"
        )