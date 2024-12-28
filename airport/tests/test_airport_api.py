from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.models import Airport
from airport.serializers import AirportSerializer
from airport.tests.base_test_class import BaseApiTest

AIRPORT_URL = reverse("airport:airports-list")


def get_retrieve_airport_url(airport_id: int) -> str:
    """
    Helper function to get the URL for retrieving a specific airport.

    Args:
        airport_id (int): The ID of the airport.

    Returns:
        str: The URL for retrieving the airport.
    """

    return reverse("airport:airports-detail", args=(airport_id,))


class UnauthenticatedAirporteApiTest(BaseApiTest):
    """
    Test class to check API access without authentication.

    Verifies that the airport API is accessible only after authentication.
    """

    def test_auth_required(self):
        """
        Test suite for airport API access without authentication.
        """

        response = self.client.get(AIRPORT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeApiTest(BaseApiTest):
    """
    Test class to check API access for authenticated users.

    Verifies operations like viewing and filtering airports for authenticated users.
    """

    def setUp(self):
        """
        Sets up test users and airports for testing API requests.
        """

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
        """
        Tests if authenticated users can retrieve a list of all airports.
        """

        response = self.client.get(AIRPORT_URL)
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_airport(self):
        """
        Tests if authenticated users can retrieve a specific airport by its ID.
        """

        url = get_retrieve_airport_url(self.airport.id)
        serializer = AirportSerializer(self.airport)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airport_by_name(self):
        """
        Tests if authenticated users can filter airports by name.
        """

        response = self.client.get(AIRPORT_URL, {"name": "second"})
        airports = Airport.objects.filter(name__icontains="second")
        serializer = AirportSerializer(airports, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_airport_by_city(self):
        """
        Tests if authenticated users can filter airports by city.
        """

        response = self.client.get(AIRPORT_URL, {"city": "lviv"})
        airports = Airport.objects.filter(closest_big_city__icontains="lviv")
        serializer = AirportSerializer(airports, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_airport_forbidden(self):
        """
        Tests if a 403 Forbidden status is returned when trying to create an airport by a regular user.
        """

        payload = {"name": "test_airport", "closest_big_city": "test_city"}
        response = self.client.post(AIRPORT_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTests(BaseApiTest):
    """
    Test class to check API operations for the admin user.

    Verifies that the admin can create airports via the API.
    """

    def setUp(self):
        """
        Sets up an admin user for testing API operations.
        """

        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)
        self.airport = Airport.objects.create(
            name="airport", closest_big_city="closest_big_city"
        )

    def test_create_airport(self):
        """
        Tests if the admin can create a new airport via the API.
        """

        payload = {"name": "test_airport", "closest_big_city": "test_city"}
        response = self.client.post(AIRPORT_URL, payload, format="json")
        airport = Airport.objects.get(id=response.data["id"])
        serializer = AirportSerializer(airport)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_update_airport(self):
        """
        Test that an admin user can update an airport resource.
        """

        payload_update = {"name": "updated_airport", "closest_big_city": "updated_city"}
        url = get_retrieve_airport_url(self.airport.id)
        response = self.client.put(url, payload_update, format="json")

        self.airport.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.airport.name, "updated_airport")
        self.assertEqual(self.airport.closest_big_city, "updated_city")
        self.assertEqual(response.data["name"], "updated_airport")
        self.assertEqual(response.data["closest_big_city"], "updated_city")

    def test_partial_update_airport(self):
        """
        Test that an admin user can partially update an airport resource.
        """

        payload = {"closest_big_city": "partially_updated_city"}
        url = get_retrieve_airport_url(self.airport.id)
        response = self.client.patch(url, payload, format="json")
        self.airport.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.airport.closest_big_city, "partially_updated_city")
        self.assertEqual(response.data["closest_big_city"], "partially_updated_city")

    def test_delete_airport(self):
        """
        Test that an admin user can delete an airport resource.
        """

        url = get_retrieve_airport_url(self.airport.id)
        response_delete = self.client.delete(url)

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
