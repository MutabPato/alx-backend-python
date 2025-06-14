from rest_framework import serializers
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    Only exposes necessary fields for API readability
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['username', 'email']

class MessageSerializer(serializers.ModelSerializer):
    """
    Message model serializer
    Uses SlugRelatedField for sender and receiver for cleaner represntation
    in the brwosable API (shows username instead of ID).
    """
    sender = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    receiver = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'parent_message', 'content', 'timestamp', 'edited', 'edited_at']
        read_only_fields = ['timestamp', 'edited', 'edited_at']


class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification model serializer
    Links User and Message models
    """
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    message = serializers.PrimaryKeyRelatedField(
        queryset=Message.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Notification
        fields = ['id', 'detail', 'user', 'message', 'created_at', 'is_read']
        read_only_fields = ['created_at']

class MessageHistorySerializer(serializers.ModelSerializer):
    """
    MessageHistory model serializer
    Is read-only as history records shouldn't be modified
    """
    message = serializers.PrimaryKeyRelatedField(read_only=True)
    edited_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = MessageHistory
        fields = ['id', 'message', 'edited_by', 'old_content', 'created_at']
        read_only_field = ['message', 'edited_by', 'old_content', 'created_at']