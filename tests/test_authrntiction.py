from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class AuthenticationTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username="testuser",
            password="qaz2wsx3edc",
            first_name="test",
            last_name="User",
        )
        self.protected_url = reverse("kitchen_core:dish-list")

    def test_redirect_for_authentication(self):
        response = self.client.get(self.protected_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.protected_url}")

    def test_successful_login(self):
        login = self.client.login(username="testuser", password="qaz2wsx3edc")
        self.assertTrue(login)

        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username="testuser", password="testpass123")
        self.client.logout()

        response = self.client.get(self.protected_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.protected_url}")
