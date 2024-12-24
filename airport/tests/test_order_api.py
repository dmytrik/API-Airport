from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight
)


ORDER_URL = reverse("airport:order-list")


class UnauthenticatedOrderApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test1234"
        )
        self.client.force_authenticate(self.user)



    def test_create_order_without_tickets(self):
        payload = {
            "user": self.user.id
        }
        response = self.client.post(ORDER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_tickets(self):
        airplane_type = AirplaneType.objects.create(
            name="test_air_type"
        )
        airplane = Airplane.objects.create(
            name="test_airplane",
            airplane_type=airplane_type,
            rows=15,
            seats_in_row=10
        )
        source = Airport.objects.create(
            name="first_test_airport",
            closest_big_city="Kyiv"
        )
        destination = Airport.objects.create(
            name="second_test_airport",
            closest_big_city="Lviv"
        )
        route = Route.objects.create(
            source=source,
            destination=destination,
            distance=450
        )
        flight = Flight.objects.create(
            route=route,
            airplane=airplane,
            departure_time=datetime(
                2024,
                12,
                24,
                16,
                0,
                0
            ),
            arrival_time=datetime(
                2024,
                12,
                24,
                22,
                0,
                0,
            )
        )
        payload = {
            "user": self.user.id,
            "tickets": [
                {
                    "row": 4,
                    "seat": 5,
                    "flight": flight.id
                }
            ]
        }

        response = self.client.post(ORDER_URL, payload)
        print(f"response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
