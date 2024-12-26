from rest_framework.test import APITestCase
from django.core.cache import cache


class BaseApiTest(APITestCase):
    """
    This class is created to clear the cache after each test
    """

    def tearDown(self):
        cache.clear()
