from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class UserManagerTests(TestCase):
    """
    Test suite for the custom UserManager in the user model.

    This class includes tests for creating users and superusers, ensuring
    that the custom manager handles user creation correctly, including edge
    cases like missing or invalid email addresses.
    """

    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "password123"

    def test_create_user(self):
        """
        Test creating a regular user.

        This test verifies that a user can be created with valid email and password,
        and that the user is not marked as staff or a superuser by default.
        """
        user = get_user_model().objects.create_user(
            email=self.email, password=self.password
        )
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        Test creating a superuser.

        This test ensures that a superuser is created with valid email and password
        and is correctly marked as staff and a superuser.
        """
        user = get_user_model().objects.create_superuser(
            email=self.email, password=self.password
        )
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email(self):
        """
        Test creating a user without an email address.

        This test verifies that attempting to create a user without an email raises
        a ValueError, as an email is required.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None, password=self.password
            )

    def test_create_user_with_invalid_email(self):
        """
        Test creating a user with an invalid email address.

        This test checks that an invalid email is stored as-is (e.g., without validation)
        and ensures the email is saved in lowercase format.
        """
        invalid_email = "invalid_email"
        user = get_user_model().objects.create_user(
            email=invalid_email, password=self.password
        )
        self.assertEqual(user.email, invalid_email.lower())

    def test_create_superuser_with_no_is_staff(self):
        """
        Test creating a superuser without is_staff set to True.

        This test verifies that a ValueError is raised if is_staff is not explicitly
        set to True when creating a superuser.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=self.email, password=self.password, is_staff=False
            )

    def test_create_superuser_with_no_is_superuser(self):
        """
        Test creating a superuser without is_superuser set to True.

        This test ensures that a ValueError is raised if is_superuser is not explicitly
        set to True when creating a superuser.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=self.email, password=self.password, is_superuser=False
            )

    def test_user_email_uniqueness(self):
        """
        Test email uniqueness for users.

        This test checks that attempting to create a user with an email that already
        exists in the database raises an IntegrityError, ensuring email uniqueness.
        """
        get_user_model().objects.create_user(
            email=self.email, password=self.password
        )
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                email=self.email, password="newpassword123"
            )

    def test_user_email_case_insensitivity(self):
        """
        Test email case insensitivity.

        This test ensures that email addresses are treated as case-insensitive,
        and users with emails differing only in case are considered duplicates.
        """
        user1 = get_user_model().objects.create_user(
            email="TESTUSER@EXAMPLE.COM", password=self.password
        )
        user2 = get_user_model().objects.create_user(
            email="testuser@example.com", password=self.password
        )
        self.assertEqual(user1.email.lower(), user2.email.lower())
