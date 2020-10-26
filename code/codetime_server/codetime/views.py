from rest_framework import generics
from .request_handlers import handle_user_post, handle_get_file_logs, handle_log_file_post
from rest_framework.response import Response


class UserView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    User View
    """

    def post(self, request, *args, **kwargs):
        """
        User post request
        """
        response = handle_user_post(request)
        return Response(data=response, status=response.get("status", 201))


class TimeLogView(generics.ListAPIView, generics.CreateAPIView):
    """
    TimeLog View
    """

    def post(self, request, *args, **kwargs):
        """
        TimeLog post request
        """
        response = handle_log_file_post(request)
        return Response(data=response, status=response.get("status", 201))

    def get(self, request, *args, **kwargs):
        """
        TimeLog get request
        """
        response = handle_get_file_logs(request)
        return Response(data=response, status=response.get("status", 200))
