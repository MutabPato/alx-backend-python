from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.decorators import login_reqired

@login_reqired
def delete_user(request):
    if request.method == 'DELETE':
        user = request.user
        logout(request) # Remove the authenticated user's ID from the request and flush their session data.
        user.delete()
        return HttpResponse("User deleted successfully")
    else:
        return HttpResponse("Method not allowed")
