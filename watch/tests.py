from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watch.api import serializers
from watch import models


class StreamPlatformTestCaseAdmin(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username='admin', password='TestAdmin@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_post_create(self):
        data = {
            "name": "Netshit",
            "about": "Sh111y platform",
            "website": "https://wwww.netshit.com"
        }
        response = self.client.post(reverse('stream-platform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StreamPlatformTestCaseUser(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='user', password='TestUser@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="TestPlatform", about="Tests",
                                                           website="https://www.tests.com")

    def test_post_create(self):
        data = {
            "name": "Netshit",
            "about": "Sh111y platform",
            "website": "https://wwww.netshit.com"
        }
        response = self.client.post(reverse('stream-platform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list(self):
        response = self.client.get(reverse('stream-platform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        response = self.client.get(reverse('stream-platform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
