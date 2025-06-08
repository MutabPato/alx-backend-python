from datetime import datetime, time
import os
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


class RequestLoggingMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        log_file_path = os.path.join(parent_dir, 'requests.log')

        with open(log_file_path, 'a') as log_file:
            log = f"\n{datetime.now()} - User: {request.user} - Path: {request.path}"
            log_file.write(log)
        response = self.get_response(request)
        return response
    

class RestrictAccessByTimeMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        to_time = time(21, 0, 0)
        from_time = time(18, 0, 0)

        if from_time <= current_time <= to_time:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        response = self.get_response(request)
        return response