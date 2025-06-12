from .models import User
from chats.serializers import UserDetailSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


# Using DRF alternatively to 'def delete_user' as described in task


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object() # Retrieves the user object based on the ID in the URL
        user.is_active = False # Sets the user active status to false
        user.save() # Saves the changes to the database
        return Response(status=status.HTTP_204_NO_CONTENT)
