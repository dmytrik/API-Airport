from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


FLIGHT_URL = reverse("airport:flight-list")


class UnauthenticatedFlightApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(FLIGHT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email = "test@test.com",
            password = "test1234"
        )
        self.client.force_authenticate(self.user)

    def test_flight_list(self):
        ...
