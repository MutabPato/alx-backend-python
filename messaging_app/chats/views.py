from rest_framework import viewsets, permissions, serializers
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    Viewset for listing conversations and listing conversations
    for authenticated users.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Ensures a user only sees conversations they are a participant of
        """
        if self.request.user.is_authenticated:
            return Conversation.objects.filter(participants=self.request.user).distinct()
        return Conversation.objects.none()
    
    def perform_create(self, serializer):
        """
        add the creating user as a participant if not explicity provided
        """
        conversation = serializer.save()
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    Viewset for listing messages
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter messages to only those within a conversation the current user is part of
        """
        if self.request.user.is_authenticated:
            user_conversations = Conversation.objects.filter(participants=self.request.user)

            # filter by a specific conversation (e.g., /messages/?conversation_if=<uuid>)
            conversation_id = self.request.query_params.get('conversation_id')
            if conversation_id:
                try:
                    conversation = user_conversations.get(conversation_id=conversation_id)
                    return Message.objects.filter(conversation=conversation).order_by('created_at')
                except Conversation.DoesNotExist:
                    return Message.objects.none()

            # if no specific conversation_id, return all messages from user's conversations
            return Message.objects.filter(conversation__in=user_conversations).order_by('created_at')
        return Message.objects.none()
    
    def perform_create(self, serializer):
        """
        Automatically assign authenticated user as sender
        """
        conversation_id = self.request.data.get('conversation_id')
        if conversation_id:
            try:
                conversation = Conversation.objects.filter(
                    participants=self.request.user, conversation_id=conversation_id
                    ).first()
                if not conversation:
                    raise serializers.ValidationError(
                        {"conversation_id": "Invalid conversation ID or you are not a participant."}
                        )
                
                serializer.save(sender=self.request.user, conversation=conversation)
            
            except ValueError:
                raise serializers.ValidationError(
                    {"conversation_id": "Conversation ID is required."}
                    )
        
    def perform_update(self, serializer):
        """
        Prevents users from changing sender or conversation of existing messages.
        """
        if serializer.instance.sender != self.request.user:
            raise permissions.PermissionDenied("You cannot update messages sent by others")

        # prevent users from changing the sender or conversation of existing messages
        if 'conversation' in serializer.validated_data and serializer.validated_data['conversation'] != serializer.instance.conversation:
            raise permissions.PermissionDenied("You cannot change the conversation of a message.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensures only the sender can delete their own message
        """
        if instance.sender != self.request.user:
            raise permissions.PermissionDenied("You are not allowed to delete messages sent by others.")
        instance.delete()