from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from airport.models import (
    Airport,
    Route,
)
from airport.serializers import RouteListDetailSerializer, RouteSerializer

ROUTE_URL = reverse("airport:router-list")


def get_retrieve_router_url(router_id: int):
    return reverse("airport:router-detail", args=(router_id,))


class UnauthenticatedTicketApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedtOrderApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@mail.com", password="test1234"
        )
        self.client.force_authenticate(self.user)
        self.source = Airport.objects.create(
            name="first_test_airport", closest_big_city="Kyiv"
        )
        self.destination = Airport.objects.create(
            name="second_test_airport", closest_big_city="Lviv"
        )
        self.second_source = Airport.objects.create(
            name="third_test_airport", closest_big_city="Poltava"
        )
        self.second_destination = Airport.objects.create(
            name="fourth_test_airport", closest_big_city="Dnipro"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=450
        )
        self.second_route = Route.objects.create(
            source=self.second_source, destination=self.second_destination, distance=450
        )

    def test_route_list(self):
        response = self.client.get(ROUTE_URL)
        routers = Route.objects.all()
        serializer = RouteListDetailSerializer(routers, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_router_forbidden(self):
        payload = {
            "source": self.second_destination.id,
            "destination": self.source.id,
            "distance": 350,
        }
        response = self.client.post(ROUTE_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_router(self):
        url = get_retrieve_router_url(self.route.id)
        serializer = RouteListDetailSerializer(self.route)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_route_by_source(self):
        response = self.client.get(ROUTE_URL, {"source": "kyiv"})
        flights = Route.objects.filter(source__closest_big_city__icontains="kyiv")
        serializer = RouteListDetailSerializer(flights, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_route_by_destination(self):
        response = self.client.get(ROUTE_URL, {"destination": "dnipro"})
        flights = Route.objects.filter(
            destination__closest_big_city__icontains="dnipro"
        )
        serializer = RouteListDetailSerializer(flights, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_route_forbidden(self):
        payload = {
            "source": self.source.id,
            "destination": self.destination.id,
            "distance": 350,
        }
        response = self.client.post(ROUTE_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)

        self.source = Airport.objects.create(
            name="first_test_airport", closest_big_city="Kyiv"
        )
        self.destination = Airport.objects.create(
            name="second_test_airport", closest_big_city="Lviv"
        )

    def test_create_route(self):
        payload = {
            "source": self.source.id,
            "destination": self.destination.id,
            "distance": 350,
        }
        response = self.client.post(ROUTE_URL, payload, format="json")
        route = Route.objects.get(id=response.data["id"])
        serializer = RouteSerializer(route)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
