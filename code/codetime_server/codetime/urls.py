from django.conf.urls import url
from .views import UserView, TimeLogView


urlpatterns = [
    url('user/', UserView.as_view(), name='user_endpoint'),
    url('timelog/', TimeLogView.as_view(), name='timelog_url')
]
