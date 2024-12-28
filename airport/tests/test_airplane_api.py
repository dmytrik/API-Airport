from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.models import Airplane, AirplaneType
from airport.serializers import AirplaneSerializer, AirplaneListDetailSerializer
from airport.tests.base_test_class import BaseApiTest

AIRPLANE_URL = reverse("airport:airplanes-list")


def get_retrieve_airplane_url(airplane_id: int) -> str:
    """
    Helper function to get the URL for retrieving a specific airplane.

    Args:
        airplane_id (int): The ID of the airplane.

    Returns:
        str: The URL for retrieving the airplane.
    """

    return reverse("airport:airplanes-detail", args=(airplane_id,))


class UnauthenticatedAirplaneApiTest(BaseApiTest):
    """
    Test suite for airplane API access without authentication.
    """

    def test_auth_required(self):
        """
        Test that airplane API endpoints require authentication.
        """

        response = self.client.get(AIRPLANE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTest(BaseApiTest):
    """
    Test suite for authenticated access to airplane API endpoints.
    """

    def setUp(self):
        """
        Set up test data for authenticated airplane API tests.
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
        self.second_airplane = Airplane.objects.create(
            name="test_airplane_second",
            airplane_type=self.airplane_type,
            rows=20,
            seats_in_row=12,
        )

    def test_list_airplane(self):
        """
        Test that authenticated users can list all airplanes.
        """

        response = self.client.get(AIRPLANE_URL)
        airplanes = Airplane.objects.all()
        serializer = AirplaneListDetailSerializer(airplanes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_airplane(self):
        """
        Test that authenticated users can retrieve details of a specific airplane.
        """

        url = get_retrieve_airplane_url(self.airplane.id)
        serializer = AirplaneListDetailSerializer(self.airplane)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airplane_by_name(self):
        """
        Test that airplanes can be filtered by name.
        """

        response = self.client.get(AIRPLANE_URL, {"name": "second"})
        airplanes = Airplane.objects.filter(name__icontains="second")
        serializer = AirplaneListDetailSerializer(airplanes, many=True)
        self.assertEqual(response.data["results"], serializer.data)


class AdminAirplaneTests(BaseApiTest):
    """
    Test suite for administrative operations on the Airplane API.

    Covers creation of airplane resources by an admin user.
    """

    def setUp(self):
        """
        Setup method to create an admin user and airplane type for testing.
        """

        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)

        self.airplane_type = AirplaneType.objects.create(name="test_air_type")
        self.airplane = Airplane.objects.create(
            name="airplane", rows=22, seats_in_row=10, airplane_type=self.airplane_type
        )

    def test_create_airplane(self):
        """
        Test that an admin user can create an airplane resource.
        """

        payload = {
            "name": "test_airplane",
            "rows": 20,
            "seats_in_row": 10,
            "airplane_type": self.airplane_type.id,
        }
        response = self.client.post(AIRPLANE_URL, payload, format="json")
        airplane = Airplane.objects.get(id=response.data["id"])
        serializer = AirplaneSerializer(airplane)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_update_airplane(self):
        """
        Test that an admin user can update an airplane resource.
        """

        payload = {
            "name": "updated_airplane",
            "rows": 25,
            "seats_in_row": 12,
            "airplane_type": self.airplane_type.id,
        }
        url = get_retrieve_airplane_url(self.airplane.id)
        response_update = self.client.put(url, payload, format="json")

        self.airplane.refresh_from_db()
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(self.airplane.name, "updated_airplane")
        self.assertEqual(self.airplane.rows, 25)
        self.assertEqual(self.airplane.seats_in_row, 12)
        self.assertEqual(response_update.data["name"], "updated_airplane")
        self.assertEqual(response_update.data["rows"], 25)
        self.assertEqual(response_update.data["seats_in_row"], 12)

    def test_partial_update_airplane(self):
        """
        Test that an admin user can partially update an airplane resource.
        """

        payload = {"rows": 30}
        url = get_retrieve_airplane_url(self.airplane.id)
        response_partial_update = self.client.patch(url, payload, format="json")

        self.airplane.refresh_from_db()
        self.assertEqual(response_partial_update.status_code, status.HTTP_200_OK)
        self.assertEqual(self.airplane.rows, 30)
        self.assertEqual(response_partial_update.data["rows"], 30)
        self.assertEqual(response_partial_update.data["name"], self.airplane.name)
        self.assertEqual(
            response_partial_update.data["seats_in_row"], self.airplane.seats_in_row
        )

    def test_delete_airplane(self):
        """
        Test that an admin user can delete an airplane resource.
        """

        payload = {
            "name": "test_airplane",
            "rows": 20,
            "seats_in_row": 10,
            "airplane_type": self.airplane_type.id,
        }
        response_create = self.client.post(AIRPLANE_URL, payload, format="json")
        airplane = Airplane.objects.get(id=response_create.data["id"])

        url = get_retrieve_airplane_url(airplane.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
