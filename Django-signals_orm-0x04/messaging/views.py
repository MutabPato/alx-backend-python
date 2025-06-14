from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions
from .models import Message, Notification, MessageHistory
from .serializers import UserSerializer, MessageSerializer, NotificationSerializer, MessageHistorySerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@login_required
@csrf_exempt
def delete_user(request):
    """
    Deletes a user account
    """
    if request.method == 'DELETE':
        user = request.user
        logout(request) # Remove the authenticated user's ID from the request and flush their session data.
        user.delete()
        return HttpResponse("User deleted successfully", status=status.HTTP_204_NO_CONTENT)
    else:
        return HttpResponse("Method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or listed
    Only allows readonly for security.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    Users can create, list, retrieve, update, and delete messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Custom queryset to ensure users only see their own messages(sent or received)
        Admins can see all
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Message.objects.select_related('parent_message').all()
        
        return Message.objects.select_related('parent_message').filter(sender=self.request.user) | Message.objects.select_related('parent_message').filter(receiver=self.request.user)
        
    
    def perform_create(self, serializer):
        """
        Automatically sets the sender of the message to the current authenticated user
        """
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        """
        Set 'edited' to True when a message is updated.
        The signal 'log_message_edit' will handle 'edited_at' and 'MessageHistory'
        """
        # Making sure the user is the sender of the message being updated
        if serializer.instance.sender != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to edit this message.")
        serializer.save(edited=True)

    def perform_destroy(self, instance):
        """
        Ensure only the sender or an admin can delete a message.
        """
        if instance.sender != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to delte this message.")
        instance.delete()   

class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notifications to be viewed , created or updated.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Custom queryset to ensure users only see their own notifications.
        Admins can see all Notifications.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Notification.objects.all()
        return Notification.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Notifications are primarily created by signals
        If a user creates one directly via API, ensure it's for themselves.
        """
        if serializer.validated_data['user'] != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You can only create notifications for yourself.")
        serializer.save()

    def perform_update(self, serializer):
        """
        Ensure users can only update their own notifications.
        """
        if serializer.instance.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to edit this notification")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensure users can only delete their own notifications.
        """
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to delte this notification.")
        instance.delete()     

class MessageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows message history to be viewed.
    History records are read-only and cannot be created, updated, or deleted via API.
    """
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Custom queryset to allow users to see history only for messages they sent or received.
        Admins can see all history.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return MessageHistory.objects.all()
        return MessageHistory.objects.filter(message__sender=self.request.user) | MessageHistory.objects.filter(message__receiver=self.request.user)
