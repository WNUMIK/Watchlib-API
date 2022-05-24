from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):

    def test_post_register(self):
        data = {
            "username": "testcase",
            "email": "test@case.com",
            "password": "TestCase@123",
            "password2": "TestCase@123"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="example", password="Example@123")

    def test_post_login(self):
        data = {
            "username": "example",
            "password": "Example@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_logout(self):
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
