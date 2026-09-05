from django.test import TestCase
from django.contrib.auth.models import User


class LandingPageTest(TestCase):
    def test_landing_index_unauthenticated_shows_auth_forms(self):
        """Test home page / renders signup and login forms for unauthenticated visitors."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/index.html")
        self.assertContains(response, "Log In to Your Account")
        self.assertContains(response, "Create New Account")

    def test_landing_index_authenticated_shows_welcome(self):
        """Test home page / shows welcome banner and create actions for logged in user."""
        user = User.objects.create_user("john", "john@test.com", "pass123")
        self.client.force_login(user)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome Back, john!")
        self.assertContains(response, "Create New Birthday Page")
