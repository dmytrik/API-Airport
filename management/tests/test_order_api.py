from datetime import datetime

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.tests.base_test_class import BaseApiTest
from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
)
from management.models import (
    Flight,
    Order,
    Ticket
)
from management.serializers import (
    OrderListSerializer,
    OrderSerializer
)


ORDER_URL = reverse("management:orders-list")

def get_retrieve_order_url(order_id: int):
    """
    Returns the URL for retrieving a specific order by its ID.

    Args:
        order_id (int): The ID of the order to retrieve.

    Returns:
        str: The URL for the order detail view.
    """
    return reverse("management:orders-detail", args=(order_id,))


class UnauthenticatedOrderApiTest(BaseApiTest):
    """
    Test suite for the order API without authentication.
    """

    def test_auth_required(self):
        """
        Test that authentication is required to access the order API.
        """
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(BaseApiTest):
    """
    Test suite for the order API with authentication.
    """

    def setUp(self):
        """
        Set up test data and authenticate the user.
        """
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
            ),
        )
        self.ticket = Ticket.objects.create(row=7, seat=9, flight=self.flight)
        self.order = Order.objects.create(
            user=self.user,
        )
        self.order.tickets.add(self.ticket)
        self.payload_without_tickets = {"tickets": []}
        self.payload_with_tickets = {
            "tickets": [{"row": 4, "seat": 5, "flight": self.flight.id}]
        }
        self.update_payload = payload = {
            "tickets": [
                {"row": 4, "seat": 5, "flight": self.flight.id},
                {"row": 3, "seat": 4, "flight": self.flight.id},
            ]
        }
        self.invalid_payload = {
            "tickets": [{"row": 16, "seat": 11, "flight": self.flight.id}]
        }

    def test_create_order_without_tickets(self):
        """
        Test creating an order without providing any tickets.
        """
        response = self.client.post(
            ORDER_URL,
            self.payload_without_tickets,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_tickets(self):
        """
        Test creating an order with valid ticket information.
        """
        response = self.client.post(
            ORDER_URL,
            self.payload_with_tickets,
            format="json"
        )
        order = Order.objects.get(id=response.data["id"])
        serializer = OrderListSerializer(order)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_update_order_with_tickets(self):
        """
        Test updating an existing order by adding new tickets.
        """
        url = get_retrieve_order_url(self.order.id)
        response = self.client.put(url, self.update_payload, format="json")

        self.order.refresh_from_db()
        serializer = OrderSerializer(self.order)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_order(self):
        """
        Test deleting an order.
        """
        url = get_retrieve_order_url(self.order.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_order_with_invalid_data_tickets(self):
        """
        Test that an order cannot be created with invalid ticket data.

        This test ensures that when the ticket data in the order contains invalid
        seat or row values (e.g., row 16 and seat 11, which are outside the valid
        range for the flight), the API returns a 400 Bad Request status code, indicating
        that the provided ticket information is not valid.
        """
        response = self.client.post(ORDER_URL, self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_order(self):
        """
        Test retrieving a specific order's details.
        """
        url = get_retrieve_order_url(self.order.id)
        response = self.client.get(url)
        serializer = OrderListSerializer(self.order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
