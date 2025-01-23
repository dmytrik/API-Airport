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
from management.serializers import TicketSerializer


TICKET_URL = reverse("management:tickets-list")

def get_retrieve_ticket_url(ticket_id: int):
    """
    Returns the URL for retrieving a specific ticket by its ID.

    Args:
        ticket_id (int): The ID of the ticket to retrieve.

    Returns:
        str: The URL for the ticket detail view.
    """
    return reverse("management:tickets-detail", args=(ticket_id,))


class UnauthenticatedTicketApiTest(BaseApiTest):
    """
    Test suite for the ticket API without authentication.
    """

    def test_auth_required(self):
        """
        Test that authentication is required to access the ticket API.
        """
        response = self.client.get(TICKET_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTicketApiTest(BaseApiTest):
    """
    Test suite for the ticket API with authentication.
    """

    def setUp(self):
        """
        Set up test data and authenticate the user.
        """
        self.user = get_user_model().objects.create_user(
            email="test@mail.com", password="test1234"
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
        self.first_ticket = Ticket.objects.create(row=7, seat=9, flight=self.flight)
        self.second_ticket = Ticket.objects.create(row=8, seat=10, flight=self.flight)
        self.order = Order.objects.create(
            user=self.user,
        )
        self.order.tickets.add(self.first_ticket, self.second_ticket)
        self.payload = {"row": 2, "seat": 2, "flight": self.flight.id}

    def test_ticket_list(self):
        """
        Test listing all tickets.
        """
        response = self.client.get(TICKET_URL)
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_ticket_not_allowed(self):
        """
        Test that creating a ticket via the API is not allowed.
        """
        response = self.client.post(TICKET_URL, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_ticket(self):
        """
        Test retrieving a specific ticket's details.
        """
        url = get_retrieve_ticket_url(self.first_ticket.id)
        serializer = TicketSerializer(self.first_ticket)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
