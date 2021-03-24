from django.db import models
from login_and_registration.models import User

class MessageManager(models.Manager):
    def message_validator(self, post_data):
        message_errors = {}
        if len(post_data['message']) < 1:
            message_errors['message'] = "Cannot post a blank message."
        return message_errors

class CommentManager(models.Manager):
    def comment_validator(self, post_data):
        comment_errors = {}
        if len(post_data['comment']) < 1:
            comment_errors['comment'] = "Cannot post a blank comment."
        return comment_errors

class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()