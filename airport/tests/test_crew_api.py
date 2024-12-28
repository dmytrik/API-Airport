from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.models import Crew
from airport.serializers import CrewSerializer
from airport.tests.base_test_class import BaseApiTest


CREW_URL = reverse("airport:crews-list")


class UnauthenticatedCrewApiTest(BaseApiTest):
    """
    Test class to check crew API access without authentication.

    Verifies that the crew API is accessible only after authentication.
    """

    def test_auth_required(self):
        """
        Test suite for crew API access without authentication.
        """

        response = self.client.get(CREW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTest(BaseApiTest):
    """
    Test class to check crew API access for authenticated users.

    Verifies operations like viewing and filtering crew members for authenticated users.
    """

    def setUp(self):
        """
        Sets up a test user and crew members for API request testing.
        """

        self.user = get_user_model().objects.create_user(
            email="test@mail.com", password="test1234"
        )
        self.client.force_authenticate(self.user)
        self.crew = Crew.objects.create(
            first_name="test_first_name", last_name="test_last_name"
        )
        self.second_crew = Crew.objects.create(
            first_name="test_name", last_name="second_name"
        )

    def test_list_crew(self):
        """
        Tests if authenticated users can retrieve a list of all crew members.
        """

        response = self.client.get(CREW_URL)
        crew = Crew.objects.all()
        serializer = CrewSerializer(crew, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_crew_forbidden(self):
        """
        Tests if a 403 Forbidden status is returned when trying to create a crew member by a regular user.
        """

        payload = {"first_name": "alan", "last_name": "balan"}
        response = self.client.post(CREW_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewTests(BaseApiTest):
    """
    Test class to check crew API operations for the admin user.

    Verifies that the admin user can create crew members via the API.
    """

    def setUp(self):
        """
        Sets up an admin user for testing API operations.
        """

        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)
        self.crew = Crew.objects.create(first_name="first_name", last_name="last_name")

    def test_create_crew(self):
        """
        Tests if the admin user can create a new crew member via the API.
        """

        payload = {"first_name": "alan", "last_name": "balan"}
        response = self.client.post(CREW_URL, payload, format="json")
        crew = Crew.objects.get(id=response.data["id"])
        serializer = CrewSerializer(crew)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
