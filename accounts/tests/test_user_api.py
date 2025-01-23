from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.serializers import UserSerializer


USER_REGISTER_URL = reverse("accounts:create")
USER_MANAGE_URL = reverse("accounts:manage")

class CreateUserViewTest(APITestCase):
    """
    Test suite for the user creation API endpoint.

    This class tests the functionality of the user registration process,
    ensuring that new users can be created successfully with valid data.
    """

    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "strongpassword",
            "is_staff": False,
        }

    def test_create_user_success(self):
        """
        Test successful user creation.

        This test verifies that a new user is created successfully when
        valid data is submitted to the user registration endpoint. It also
        checks that the response contains the correct email and excludes
        the password field.
        """
        response = self.client.post(USER_REGISTER_URL, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertNotIn("password", response.data)


class ManageUserViewTest(APITestCase):
    """
    Test suite for the user management API endpoint.

    This class tests the functionality of retrieving and managing user profiles
    for authenticated users.
    """

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            email="test@mail.com",
            password="password1234"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_user_success(self):
        """
        Test retrieving the authenticated user's profile.

        This test ensures that an authenticated user can retrieve their profile
        successfully from the user management endpoint. It compares the response
        data with the expected serialized user data.
        """
        response = self.client.get(USER_MANAGE_URL)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
