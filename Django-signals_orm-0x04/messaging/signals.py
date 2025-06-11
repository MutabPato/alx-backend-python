import logging
from django.db.models.signals import post_save
from .models import Message, Notification
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=Message)
def message_post_save_receiver(sender, instance, created, **kwargs):
    """
    Triggers a notification when a new Message instance is created.
    listens for new messages and automatically creates a notification for the receiving user.
    """
    if created:
        try:
            Notification.objects.create(
                detail="You have a new message from {instance.sender.username}!",
                user=instance.receiver,
                message=instance
                )
            print(
                f"Notification created for {instance.receiver.username} "
                f"due to new message from {instance.sender.username} (ID: {instance.id})"
            )

        except Exception as e:
            print(f"Error creating notification for message ID: {instance.id}: {e}")
