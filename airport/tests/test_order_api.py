from datetime import datetime

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Ticket,
    Order
)
from airport.serializers import OrderListSerializer
from airport.tests.base_test_class import BaseApiTest


ORDER_URL = reverse("airport:order-list")


def get_retrieve_order_url(order_id: int):
    return reverse("airport:order-detail", args=(order_id,))


class UnauthenticatedOrderApiTest(BaseApiTest):

    def test_auth_required(self):
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(BaseApiTest):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test1234"
        )
        self.client.force_authenticate(self.user)
        self.airplane_type = AirplaneType.objects.create(name="test_air_type")
        self.airplane = Airplane.objects.create(
            name="test_airplane",
            airplane_type=self.airplane_type,
            rows=15,
            seats_in_row=10,
        )
        self.source = Airport.objects.create(
            name="first_test_airport", closest_big_city="Kyiv"
        )
        self.destination = Airport.objects.create(
            name="second_test_airport", closest_big_city="Lviv"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=450
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=datetime(2024, 12, 24, 16, 0, 0),
            arrival_time=datetime(
                2024,
                12,
                24,
                22,
                0,
                0,
            ),
        )
        self.ticket = Ticket.objects.create(row=7, seat=9, flight=self.flight)
        self.order = Order.objects.create(
            user=self.user,
        )
        self.order.tickets.add(self.ticket)

    def test_create_order_without_tickets(self):
        payload = {"tickets": []}
        response = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_tickets(self):
        payload = {"tickets": [{"row": 4, "seat": 5, "flight": self.flight.id}]}

        response = self.client.post(ORDER_URL, payload, format="json")
        order = Order.objects.get(id=response.data["id"])
        serializer = OrderListSerializer(order)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_order(self):
        url = get_retrieve_order_url(self.order.id)
        response = self.client.get(url)
        serializer = OrderListSerializer(self.order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
