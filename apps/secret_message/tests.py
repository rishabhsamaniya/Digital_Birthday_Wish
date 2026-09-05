from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.profiles.models import BirthdayProfile
from apps.secret_message.models import SecretMessage


class SecretMessageModelTest(TestCase):
    def setUp(self):
        self.profile = BirthdayProfile.objects.create(
            full_name="Kavya Verma",
            slug="kavya",
            birthday_date=date(1996, 11, 14)
        )
        self.secret = SecretMessage.objects.create(
            birthday_profile=self.profile,
            title="For Kavya Only 🔒",
            secret_text="You mean the world to me!",
            pin_code="1234",
            hint="Our anniversary date"
        )

    def test_secret_message_creation_and_pin_check(self):
        """Test model creation and check_pin method."""
        self.assertEqual(self.secret.title, "For Kavya Only 🔒")
        self.assertTrue(self.secret.check_pin("1234"))
        self.assertFalse(self.secret.check_pin("9999"))
        self.assertIn("Kavya Verma", str(self.secret))

    def test_no_pin_check(self):
        """Test check_pin returns True if no pin_code set."""
        no_pin_secret = SecretMessage(secret_text="Public text")
        self.assertTrue(no_pin_secret.check_pin("anything"))

    def test_profile_cascade_deletion(self):
        """Test deleting profile automatically deletes associated secret message."""
        profile_pk = self.profile.pk
        secret_pk = self.secret.pk

        self.profile.delete()

        self.assertFalse(BirthdayProfile.objects.filter(pk=profile_pk).exists())
        self.assertFalse(SecretMessage.objects.filter(pk=secret_pk).exists())


class SecretMessageDashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")
        self.profile = BirthdayProfile.objects.create(
            full_name="Rohan Mehra",
            slug="rohan",
            birthday_date=date(1994, 8, 12)
        )
        self.secret = SecretMessage.objects.create(
            birthday_profile=self.profile,
            title="Top Secret",
            secret_text="Surprise trip planned!",
            pin_code="0415"
        )

    def test_secret_detail_dashboard_view(self):
        """Test dashboard secret message detail/edit view."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:secret_message_detail", kwargs={"profile_id": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Top Secret")

    def test_secret_save_dashboard_view(self):
        """Test saving secret message form via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:secret_message_detail", kwargs={"profile_id": self.profile.pk}), {
            "title": "Top Secret Updated",
            "secret_text": "Updated secret message text!",
            "pin_code": "5678",
            "hint": "New hint"
        })
        self.assertEqual(response.status_code, 302)
        self.secret.refresh_from_db()
        self.assertEqual(self.secret.title, "Top Secret Updated")
        self.assertEqual(self.secret.pin_code, "5678")

    def test_secret_delete_dashboard_view(self):
        """Test deleting secret message via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:secret_message_delete", kwargs={"pk": self.secret.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(SecretMessage.objects.filter(pk=self.secret.pk).exists())


class SecretMessagePublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = BirthdayProfile.objects.create(
            full_name="Rohan Mehra",
            slug="rohan",
            birthday_date=date(1994, 8, 12),
            is_active=True
        )
        self.secret = SecretMessage.objects.create(
            birthday_profile=self.profile,
            title="Secret Wish",
            secret_text="You are awesome!",
            pin_code="7777"
        )

    def test_public_secret_reveal_view_get(self):
        """Test accessing /rohan/secret/ renders lock screen page."""
        response = self.client.get("/rohan/secret/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "secret_message/index.html")
        self.assertEqual(response.context["current_step"], 9)
        self.assertEqual(response.context["prev_url"], "/rohan/messages/")
        self.assertEqual(response.context["next_url"], "/rohan/wish/")

    def test_ajax_pin_verification_success(self):
        """Test AJAX PIN verification returning success."""
        response = self.client.post(
            "/rohan/secret/",
            {"pin": "7777"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["title"], "Secret Wish")
        self.assertEqual(json_data["secret_text"], "You are awesome!")

    def test_ajax_pin_verification_failure(self):
        """Test AJAX PIN verification returning failure for wrong PIN."""
        response = self.client.post(
            "/rohan/secret/",
            {"pin": "0000"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertFalse(json_data["success"])
        self.assertIn("Incorrect passcode PIN", json_data["error"])
