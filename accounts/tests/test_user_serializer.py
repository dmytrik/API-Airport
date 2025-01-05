from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from accounts.serializers import UserSerializer


class UserSerializerTest(APITestCase):
    """
    Test suite for the UserSerializer.

    This class tests the functionality of the UserSerializer, including user creation,
    updates, and validations, ensuring that serialized data is handled correctly.
    """

    def setUp(self):
        self.password = "password123"
        self.user_data = {
            "email": "testuser@example.com",
            "password": self.password,
            "is_staff": False,
        }

    def test_create_user(self):
        """
        Test creating a new user with valid data.

        This test ensures that the serializer correctly validates and creates a new user,
        properly storing the email and hashed password, and setting the is_staff field to False.
        """
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)

    def test_update_user(self):
        """
        Test updating an existing user's data.

        This test verifies that the serializer can update user data, including changing
        the email and password, while ensuring the password is securely hashed.
        """
        user = get_user_model().objects.create_user(
            email="existinguser@example.com", password="oldpassword"
        )
        new_data = {
            "email": "newemail@example.com",
            "password": "newpassword123",
        }

        serializer = UserSerializer(user, data=new_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, new_data["email"])
        self.assertTrue(updated_user.check_password(new_data["password"]))

    def test_update_user_without_password(self):
        """
        Test updating a user's email without changing the password.

        This test ensures that when a user's email is updated using the serializer, the
        existing password remains unchanged if a new password is not provided.
        """
        user = get_user_model().objects.create_user(
            email="existinguser@example.com", password="oldpassword"
        )
        new_data = {"email": "newemail@example.com"}

        serializer = UserSerializer(user, data=new_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, new_data["email"])
        self.assertTrue(updated_user.check_password("oldpassword"))

    def test_password_is_write_only(self):
        """
        Test that the password field is write-only.

        This test verifies that the password is excluded from the serialized output
        when retrieving user data, ensuring it cannot be exposed.
        """
        user = get_user_model().objects.create_user(
            email="testuser@example.com", password="password123"
        )

        serializer = UserSerializer(user)
        self.assertNotIn("password", serializer.data)

    def test_create_user_with_existing_email(self):
        """
        Test creating a user with an already existing email.

        This test checks that the serializer prevents the creation of a new user
        with an email that is already registered, returning appropriate validation errors.
        """
        get_user_model().objects.create_user(
            email="testuser@example.com", password=self.password
        )

        data = {
            "email": "testuser@example.com",
            "password": self.password,
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
