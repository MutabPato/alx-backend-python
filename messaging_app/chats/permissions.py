from rest_framework.permissions import BasePermission


class HasRoleEditor(BasePermission):
    """
    Allow access only to users with the 'editor' role in their JWT
    """
    message = "You do not have permission to perform this action (requires 'editor' role)."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        token = request.auth
        if not token:
            return False
        
        user_roles = token.get('roles', [])
        return 'editor' in user_roles

"""class MyResourceView(APIView):
    permission_classes = [IsAuthenticated, HasRoleEditor]

    def post(self, request):
        return Response({"message": "Resource created by an editor."})
"""