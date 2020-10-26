# Created by Ayushi Rajendra Kumar at 10/25/2020

# Feature: #Enter feature name here
# Enter feature description here

# Scenario: # Enter scenario name here
# Enter steps here
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.utils import json


users_data = {
    "log_user_id": 1223,
    "username": "ayushi2",
    "password": "123ayushi1",
    "api_token": "1234abcd"

}

users_data1 = {
    "username": "ayushi2",
    "password": "123ayushi1"

}


class TestPostViews(TestCase):
    """
    Tests to verify the functioning of all the POST requests in bot_server/api
    """

    def setUp(self):
        """
        Test setup for each test in this class. It is done for each of the tests
        """
        self.client = Client()
        self.user_url = reverse('user_endpoint')
        # User.objects.create_user(users_data)

    def test_get_user(self):
        """
        Test behaviour of correct POST request for creating a user
        """
        user_url = f"{self.user_url}?type=signup"
        response = self.client.post(user_url, data=json.dumps(users_data1), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
