from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def test_user_can_register(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "alice",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="alice").exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_can_login(self):
        get_user_model().objects.create_user(username="bob", password="StrongPass123!")

        response = self.client.post(
            reverse("accounts:login"),
            {"username": "bob", "password": "StrongPass123!"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

# Create your tests here.
