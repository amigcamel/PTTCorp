from django.db import models


class CommentModel(models.Model):
    username = models.CharField(max_length=20)
    message = models.CharField(max_length=200)
    post_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    ip = models.CharField(max_length=20, blank=True)
    reply = models.CharField(max_length=200, blank=True)
    reply_datetime = models.DateTimeField(null=True, blank=True)
