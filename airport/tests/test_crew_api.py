from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.models import Crew
from airport.serializers import CrewSerializer
from airport.tests.base_test_class import BaseApiTest

CREW_URL = reverse("airport:crews-list")


def get_retrieve_crew_url(crew_id: int):
    return reverse("airport:crews-detail", args=(crew_id,))


class UnauthenticatedCrewApiTest(BaseApiTest):

    def test_auth_required(self):
        response = self.client.get(CREW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedtCrewApiTest(BaseApiTest):

    def setUp(self):
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
        response = self.client.get(CREW_URL)
        crew = Crew.objects.all()
        serializer = CrewSerializer(crew, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_crew_forbidden(self):
        payload = {"first_name": "alan", "last_name": "balan"}
        response = self.client.post(CREW_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewTests(BaseApiTest):

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.client.force_authenticate(self.admin)

    def test_create_crew(self):
        payload = {"first_name": "alan", "last_name": "balan"}
        response = self.client.post(CREW_URL, payload, format="json")
        crew = Crew.objects.get(id=response.data["id"])
        serializer = CrewSerializer(crew)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
