from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    detail = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)