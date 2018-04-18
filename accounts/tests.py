from django.urls import reverse
from django.contrib.auth import models as auth_models
from rest_framework import status
from rest_framework.test import APITestCase


def get_or_create_user(is_admin, username=None):
    if username is None:
        user_count = auth_models.User.objects.count()
        username = f"user_{user_count}"
    
    return auth_models.User.objects.get_or_create(
        username=username, 
        password='secret',
        is_superuser=is_admin,
        is_staff=is_admin
    )
    

class UserTests(APITestCase):
    def test_create_user_as_admin(self):
        """Tests creating a user as an admin user

        This test is more around the testing of the custom permission class
        as the viewsets are standard.
        """
        admin, created = get_or_create_user(is_admin=True)
        self.client.force_authenticate(admin)

        url = reverse('accounts:user-list')
        data = {
            'username': 'testuser',
            'password': 'secret'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(auth_models.User.objects.count(), 2)

    def test_create_user_as_non_admin(self):
        """Tests creating a user as a non admin user

        This test is more around the testing of the custom permission class
        as the viewsets are standard.

        Non admin users are not permitted to created user instances
        """
        user, created = get_or_create_user(is_admin=False)
        self.client.force_authenticate(user)

        url = reverse('accounts:user-list')
        data = {
            'username': 'testuser',
            'password': 'secret'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_as_admin(self):
        """Tests creating a user as a non admin user

        This test is more around the testing of the custom permission class
        as the viewsets are standard.

        Non admin users are not permitted to created user instances
        """
        admin, created = get_or_create_user(is_admin=True)
        self.client.force_authenticate(admin)

        url = reverse('accounts:user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), auth_models.User.objects.count())

    def test_filter_as_non_admin(self):
        """Tests creating a user as a non admin user

        This test is more around the testing of the custom permission class
        as the viewsets are standard.

        Non admin users are not permitted to created user instances
        """
        user, created = get_or_create_user(is_admin=False)
        self.client.force_authenticate(user)

        url = reverse('accounts:user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], user.pk)