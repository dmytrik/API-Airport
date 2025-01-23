from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.models import AirplaneType
from airport.serializers import AirplaneTypeSerializer
from airport.tests.base_test_class import BaseApiTest

AIRPLANE_TYPE_URL = reverse("airport:airplane-types-list")


def get_retrieve_airplane_type_url(airplane_type_id: int) -> str:
    """
    Helper function to get the URL for retrieving a specific airplane type.

    Args:
        airplane_type_id (int): The ID of the airplane_type.

    Returns:
        str: The URL for retrieving the airplane_type.
    """
    return reverse("airport:airplane-types-detail", args=(airplane_type_id,))


class UnauthenticatedAirplaneTypeApiTest(BaseApiTest):
    """
    Test suite for airplane_type API access without authentication.
    """

    def test_auth_required(self):
        """
        Test that airplane_type API endpoints require authentication.
        """
        response = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeApiTest(BaseApiTest):
    """
    Test suite for authenticated access to airplane_type API endpoints.
    """

    def setUp(self):
        """
        Set up test data for authenticated airplane_type API tests.
        """
        self.user = get_user_model().objects.create_user(
            email="test@mail.com", password="test1234"
        )
        self.client.force_authenticate(self.user)
        self.airplane_type = AirplaneType.objects.create(name="test_air_type")
        self.second_airplane_type = AirplaneType.objects.create(
            name="test_air_type_second"
        )
        self.payload = {
            "name": "test_airplane_type",
        }

    def test_list_airplane_type(self):
        """
        Test that authenticated users can list all airplane types.
        """
        response = self.client.get(AIRPLANE_TYPE_URL)
        airplane_types = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(airplane_types, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_airplane_type(self):
        """
        Test that authenticated users can retrieve a specific airplane type by ID.
        """
        url = get_retrieve_airplane_type_url(self.airplane_type.id)
        serializer = AirplaneTypeSerializer(self.airplane_type)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airplane_type_by_name(self):
        """
        Test that airplane_types can be filtered by name.
        """
        response = self.client.get(AIRPLANE_TYPE_URL, {"name": "second"})
        airplane_types = AirplaneType.objects.filter(name__icontains="second")
        serializer = AirplaneTypeSerializer(airplane_types, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_airplane_type_forbidden(self):
        """
        Test that an authenticated user can't create a new airplane type.
        """
        response = self.client.post(AIRPLANE_TYPE_URL, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTypeTests(BaseApiTest):
    """
    Test suite for airplane_type API access for admin.
    """

    def setUp(self):
        """
        Set up test data for admin airplane_type API tests.
        """
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)
        self.airplane_type = AirplaneType.objects.create(name="airplane_type")
        self.payload = {
            "name": "test_airplane_type",
        }

    def test_create_airplane_type(self):
        """
        Test that an admin user can create a new airplane type.
        """
        response = self.client.post(AIRPLANE_TYPE_URL, self.payload, format="json")
        airplane_type = AirplaneType.objects.get(id=response.data["id"])
        serializer = AirplaneTypeSerializer(airplane_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_update_airplane_type(self):
        """
        Test that an admin user can update an airplane type resource.
        """
        url = get_retrieve_airplane_type_url(self.airplane_type.id)
        response = self.client.put(url, self.payload, format="json")

        self.airplane_type.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.airplane_type.name, "test_airplane_type")
        self.assertEqual(response.data["name"], "test_airplane_type")

    def test_delete_airplane_type(self):
        """
        Test that an admin user can delete an airplane type resource.
        """
        url = get_retrieve_airplane_type_url(self.airplane_type.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
