from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.models import Airport
from airport.serializers import AirportSerializer
from airport.tests.base_test_class import BaseApiTest

AIRPORT_URL = reverse("airport:airport-list")


def get_retrieve_airport_url(airport_id: int):
    return reverse("airport:airport-detail", args=(airport_id,))


class UnauthenticatedAirporteApiTest(BaseApiTest):

    def test_auth_required(self):
        response = self.client.get(AIRPORT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedtAirplaneTypeApiTest(BaseApiTest):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@mail.com", password="test1234"
        )
        self.client.force_authenticate(self.user)
        self.airport = Airport.objects.create(
            name="first_test_airport", closest_big_city="Kyiv"
        )
        self.second_airport = Airport.objects.create(
            name="second_test_airport", closest_big_city="Lviv"
        )

    def test_list_airport(self):
        response = self.client.get(AIRPORT_URL)
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_airport(self):
        url = get_retrieve_airport_url(self.airport.id)
        serializer = AirportSerializer(self.airport)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airport_by_name(self):
        response = self.client.get(AIRPORT_URL, {"name": "second"})
        airports = Airport.objects.filter(name__icontains="second")
        serializer = AirportSerializer(airports, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_airport_by_city(self):
        response = self.client.get(AIRPORT_URL, {"city": "lviv"})
        airports = Airport.objects.filter(closest_big_city__icontains="lviv")
        serializer = AirportSerializer(airports, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_airport_forbidden(self):
        payload = {"name": "test_airport", "closest_big_city": "test_city"}
        response = self.client.post(AIRPORT_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTests(BaseApiTest):

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)

    def test_create_airport(self):
        payload = {"name": "test_airport", "closest_big_city": "test_city"}
        response = self.client.post(AIRPORT_URL, payload, format="json")
        airport = Airport.objects.get(id=response.data["id"])
        serializer = AirportSerializer(airport)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
