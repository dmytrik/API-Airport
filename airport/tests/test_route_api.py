from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.models import Airport, Route
from airport.serializers import RouteListDetailSerializer, RouteSerializer
from airport.tests.base_test_class import BaseApiTest


ROUTE_URL = reverse("airport:routers-list")


def get_retrieve_router_url(router_id: int):
    """
    Helper function to get the URL for retrieving a specific route.

    Args:
        route_id (int): The ID of the route.

    Returns:
        str: The URL for retrieving the route.
    """

    return reverse("airport:routers-detail", args=(router_id,))


class UnauthenticatedRouteApiTest(BaseApiTest):
    """
    Test suite for route API access without authentication.

    Verifies that the route API is accessible only for authenticated users.
    """

    def test_auth_required(self):
        """
        Test suite for route API access without authentication.
        """

        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTest(BaseApiTest):
    """
    Test suite for route API access for authenticated users.

    Verifies that authenticated users can retrieve and filter routes, but cannot create them.
    """

    def setUp(self):
        """
        Sets up a test user and airport data for route API request testing.
        Creates a few airports and routes for testing the route-related operations.
        """

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
        """
        Tests that authenticated users can retrieve a list of all routes.
        """

        response = self.client.get(ROUTE_URL)
        routers = Route.objects.all()
        serializer = RouteListDetailSerializer(routers, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_router_forbidden(self):
        """
        Tests that authenticated users cannot create routes, expecting a 403 Forbidden status.
        """

        payload = {
            "source": self.second_destination.id,
            "destination": self.source.id,
            "distance": 350,
        }
        response = self.client.post(ROUTE_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_router(self):
        """
        Tests that authenticated users can retrieve the details of a specific route by its ID.
        """

        url = get_retrieve_router_url(self.route.id)
        serializer = RouteListDetailSerializer(self.route)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_route_by_source(self):
        """
        Tests that authenticated users can filter routes by the source airport's closest big city.
        """

        response = self.client.get(ROUTE_URL, {"source": "kyiv"})
        flights = Route.objects.filter(source__closest_big_city__icontains="kyiv")
        serializer = RouteListDetailSerializer(flights, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_route_by_destination(self):
        """
        Tests that authenticated users can filter routes by the destination airport's closest big city.
        """

        response = self.client.get(ROUTE_URL, {"destination": "dnipro"})
        flights = Route.objects.filter(
            destination__closest_big_city__icontains="dnipro"
        )
        serializer = RouteListDetailSerializer(flights, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_route_forbidden(self):
        """
        Tests that authenticated users cannot create routes, expecting a 403 Forbidden status.
        """

        payload = {
            "source": self.source.id,
            "destination": self.destination.id,
            "distance": 350,
        }
        response = self.client.post(ROUTE_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteTests(BaseApiTest):
    """
    Test suite for route API access by the admin user.

    Verifies that the admin user has permission to create and manage routes via the API.
    """

    def setUp(self):
        """
        Sets up an admin user and airport data for route API operations.
        """

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
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=450
        )

    def test_create_route(self):
        """
        Tests that the admin user can create a new route via the API.
        """

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

    def test_update_route(self):
        """
        Test that an admin user can update a route resource.
        """

        payload = {
            "source": self.source.id,
            "destination": self.destination.id,
            "distance": 400,
        }
        url = get_retrieve_router_url(self.route.id)
        response = self.client.put(url, payload, format="json")
        self.route.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.route.distance, 400)
        self.assertEqual(response.data["distance"], 400)

    def test_partial_update_route(self):
        """
        Test that an admin user can partially update a route resource.
        """

        payload = {"distance": 400}
        url = get_retrieve_router_url(self.route.id)
        response = self.client.patch(url, payload, format="json")
        self.route.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.route.distance, 400)
        self.assertEqual(response.data["distance"], 400)

    def test_delete_route(self):
        """
        Test that an admin user can delete a route resource.
        """

        url = get_retrieve_router_url(self.route.id)
        response_delete = self.client.delete(url)

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
