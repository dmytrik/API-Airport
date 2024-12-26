from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.models import Airplane, AirplaneType
from airport.serializers import AirplaneSerializer, AirplaneListDetailSerializer
from airport.tests.base_test_class import BaseApiTest

AIRPLANE_URL = reverse("airport:airplane-list")


def get_retrieve_airplane_url(airplane_id: int):
    return reverse("airport:airplane-detail", args=(airplane_id,))


class UnauthenticatedAirplaneApiTest(BaseApiTest):

    def test_auth_required(self):
        response = self.client.get(AIRPLANE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTest(BaseApiTest):

    def setUp(self):
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
        response = self.client.get(AIRPLANE_URL)
        airplanes = Airplane.objects.all()
        serializer = AirplaneListDetailSerializer(airplanes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_airplane(self):
        url = get_retrieve_airplane_url(self.airplane.id)
        serializer = AirplaneListDetailSerializer(self.airplane)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airplane_by_name(self):
        response = self.client.get(AIRPLANE_URL, {"name": "second"})
        airplanes = Airplane.objects.filter(name__icontains="second")
        serializer = AirplaneListDetailSerializer(airplanes, many=True)
        self.assertEqual(response.data["results"], serializer.data)


class AdminAirplaneTests(BaseApiTest):

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)

        self.airplane_type = AirplaneType.objects.create(name="test_air_type")

    def test_create_airplane(self):
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
