from datetime import datetime

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.tests.base_test_class import BaseApiTest
from airport.models import (
    Route,
    Airplane,
    AirplaneType,
    Airport,
    Crew
)
from management.models import Flight
from management.serializers import FlightListSerializer, FlightDetailSerializer

FLIGHT_URL = reverse("management:flights-list")


def detail_flight_url(id: int):
    return reverse("management:flights-detail", args=(id,))


class UnauthenticatedFlightApiTests(BaseApiTest):

    def test_auth_required(self):
        response = self.client.get(FLIGHT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTest(BaseApiTest):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test1234"
        )
        self.client.force_authenticate(self.user)
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
        self.second_source = Airport.objects.create(
            name="dnipro_airport", closest_big_city="dnipro"
        )
        self.second_destination = Airport.objects.create(
            name="poltava_airport", closest_big_city="Poltava"
        )
        self.second_route = Route.objects.create(
            source=self.second_source, destination=self.second_destination, distance=200
        )
        self.second_airplane_type = AirplaneType.objects.create(name="commercial")
        self.second_airplane = Airplane.objects.create(
            name="Boeing",
            rows=20,
            seats_in_row=10,
            airplane_type=self.second_airplane_type,
        )
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.second_crew = Crew.objects.create(first_name="Alan", last_name="Balan")
        self.second_flight = Flight.objects.create(
            route=self.second_route,
            airplane=self.second_airplane,
            departure_time=datetime(2024, 12, 26, 18, 0, 0),
            arrival_time=datetime(2024, 12, 26, 20, 0, 0),
        )
        self.second_flight.crew.add(self.crew, self.second_crew)

    def test_flight_list(self):
        response = self.client.get(FLIGHT_URL)
        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_flight_by_city_from(self):
        response = self.client.get(FLIGHT_URL, {"city_from": "dnipro"})
        flights = Flight.objects.filter(
            route__source__closest_big_city__icontains="dnipro"
        )
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_flight_by_city_to(self):
        response = self.client.get(FLIGHT_URL, {"city_to": "lviv"})
        flights = Flight.objects.filter(
            route__destination__closest_big_city__icontains="lviv"
        )
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_flight_by_departure_time(self):
        response = self.client.get(FLIGHT_URL, {"departure_time": "2024-12-25"})
        flights = Flight.objects.filter(departure_time__icontains="2024-12-25")
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_flight(self):
        url = detail_flight_url(self.second_flight.id)
        response = self.client.get(url)
        flight = Flight.objects.get(id=self.second_flight.id)
        serializer = FlightDetailSerializer(flight)
        self.assertEqual(response.data, serializer.data)

    def test_create_flight_forbidden(self):
        payload = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": datetime(2024, 12, 26, 18, 0, 0),
            "arrival_time": datetime(2024, 12, 26, 20, 0, 0),
            "crew": [self.crew.id, self.second_crew.id],
        }
        response = self.client.post(FLIGHT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightTests(BaseApiTest):

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)
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
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.second_crew = Crew.objects.create(first_name="Alan", last_name="Balan")

    def test_create_flight(self):
        payload = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": datetime(2024, 12, 26, 18, 0, 0),
            "arrival_time": datetime(2024, 12, 26, 20, 0, 0),
            "crew": [self.crew.id, self.second_crew.id],
        }
        response = self.client.post(FLIGHT_URL, payload)
        flight = Flight.objects.get(id=response.data["id"])
        crew = flight.crew.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.crew, crew)
        self.assertIn(self.second_crew, crew)
        self.assertEqual(crew.count(), 2)
