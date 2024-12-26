from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from airport.models import AirplaneType
from airport.serializers import AirplaneTypeSerializer

AIRPLANE_TYPE_URL = reverse("airport:airplane-type-list")


def get_retrieve_airplane_type_url(airplane_type_id: int):
    return reverse("airport:airplane-type-detail", args=(airplane_type_id,))


class UnauthenticatedAirplaneTypeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedtAirplaneTypeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@mail.com", password="test1234"
        )
        self.client.force_authenticate(self.user)
        self.airplane_type = AirplaneType.objects.create(name="test_air_type")
        self.second_airplane_type = AirplaneType.objects.create(
            name="test_air_type_second"
        )

    def test_list_airplane(self):
        response = self.client.get(AIRPLANE_TYPE_URL)
        airplane_types = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(airplane_types, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_airplane_type(self):
        url = get_retrieve_airplane_type_url(self.airplane_type.id)
        serializer = AirplaneTypeSerializer(self.airplane_type)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airplane_type_by_name(self):
        response = self.client.get(AIRPLANE_TYPE_URL, {"name": "second"})
        airplane_types = AirplaneType.objects.filter(name__icontains="second")
        serializer = AirplaneTypeSerializer(airplane_types, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_airplane_type_forbidden(self):
        payload = {
            "name": "test_airplane_type",
        }
        response = self.client.post(AIRPLANE_TYPE_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)

    def test_create_airplane_type(self):
        payload = {
            "name": "test_airplane_type",
        }
        response = self.client.post(AIRPLANE_TYPE_URL, payload, format="json")
        airplane_type = AirplaneType.objects.get(id=response.data["id"])
        serializer = AirplaneTypeSerializer(airplane_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
