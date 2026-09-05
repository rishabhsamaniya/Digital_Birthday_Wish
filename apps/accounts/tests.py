from django.test import TestCase
from django.contrib.auth.models import User
from apps.profiles.services.ai_wishes_service import get_ai_message_suggestions


class AccountsAuthTest(TestCase):
    def test_user_signup_get(self):
        """Test GET request to signup page renders signup form."""
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_user_signup_post_creates_account(self):
        """Test POST request to signup page registers new user and logs them in."""
        data = {
            "username": "testuser",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        }
        response = self.client.post("/accounts/signup/", data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_login_success(self):
        """Test user login with valid credentials."""
        User.objects.create_user(username="validuser", password="ValidPassword123!")
        data = {
            "username": "validuser",
            "password": "ValidPassword123!",
        }
        response = self.client.post("/accounts/login/", data)
        self.assertEqual(response.status_code, 302)


class AiWishesServiceTest(TestCase):
    def test_ai_message_suggestions_structure(self):
        """Test get_ai_message_suggestions returns 10 curated message categories."""
        suggestions = get_ai_message_suggestions()
        self.assertEqual(len(suggestions), 10)
        self.assertIn("category", suggestions[0])
        self.assertIn("message", suggestions[0])
