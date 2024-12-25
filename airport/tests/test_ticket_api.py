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
    Flight,
    Ticket,
    Order
)
from airport.serializers import TicketSerializer

TICKET_URL = reverse("airport:ticket-list")

def get_retrieve_ticket_url(ticket_id: int):
    return reverse("airport:ticket-detail", args=(ticket_id,))


class UnauthenticatedTicketApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(TICKET_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTicketApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@mail.com",
            password="test1234"
        )
        self.client.force_authenticate(self.user)
        self.airplane_type = AirplaneType.objects.create(
            name="test_air_type"
        )
        self.airplane = Airplane.objects.create(
            name="test_airplane",
            airplane_type=self.airplane_type,
            rows=15,
            seats_in_row=10
        )
        self.source = Airport.objects.create(
            name="first_test_airport",
            closest_big_city="Kyiv"
        )
        self.destination = Airport.objects.create(
            name="second_test_airport",
            closest_big_city="Lviv"
        )
        self.route = Route.objects.create(
            source=self.source,
            destination=self.destination,
            distance=450
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
            )
        )
        self.first_ticket = Ticket.objects.create(
            row=7,
            seat=9,
            flight=self.flight
        )
        self.second_ticket = Ticket.objects.create(
            row=8,
            seat=10,
            flight=self.flight
        )
        self.order = Order.objects.create(
            user=self.user,
        )
        self.order.tickets.add(self.first_ticket, self.second_ticket)

    def test_ticket_list(self):
        response = self.client.get(TICKET_URL)
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_ticket_not_allowed(self):
        payload = {
            "row": 2,
            "seat": 2,
            "flight": self.flight.id
        }
        response = self.client.post(TICKET_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_ticket(self):
        url = get_retrieve_ticket_url(self.first_ticket.id)
        serializer = TicketSerializer(self.first_ticket)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
