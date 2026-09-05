from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.profiles.models import BirthdayProfile
from apps.wishes.models import WishSubmission


class WishSubmissionModelTest(TestCase):
    def setUp(self):
        self.profile = BirthdayProfile.objects.create(
            full_name="Aarav Sharma",
            slug="aarav",
            birthday_date=date(1998, 12, 5)
        )
        self.wish = WishSubmission.objects.create(
            birthday_profile=self.profile,
            sender_name="Pooja & Family",
            message="Wishing you happiness and success always!",
            candle_blown=True,
            is_approved=True
        )

    def test_wish_submission_creation(self):
        """Test WishSubmission creation and str representation."""
        self.assertEqual(self.wish.sender_name, "Pooja & Family")
        self.assertTrue(self.wish.candle_blown)
        self.assertIn("Pooja & Family", str(self.wish))

    def test_profile_cascade_deletion(self):
        """Test deleting profile automatically deletes associated wish submissions."""
        profile_pk = self.profile.pk
        wish_pk = self.wish.pk

        self.profile.delete()

        self.assertFalse(BirthdayProfile.objects.filter(pk=profile_pk).exists())
        self.assertFalse(WishSubmission.objects.filter(pk=wish_pk).exists())


class WishSubmissionDashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")
        self.profile = BirthdayProfile.objects.create(
            full_name="Simran Kapoor",
            slug="simran",
            birthday_date=date(1999, 5, 20)
        )
        self.wish = WishSubmission.objects.create(
            birthday_profile=self.profile,
            sender_name="Kabir",
            message="Happy Birthday Simran!",
            is_approved=True
        )

    def test_wish_list_dashboard_view(self):
        """Test dashboard wishes list view."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:wish_list", kwargs={"profile_id": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kabir")

    def test_wish_toggle_approval_dashboard_view(self):
        """Test toggling public approval on a wish submission."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:wish_toggle_approval", kwargs={"pk": self.wish.pk}))
        self.assertEqual(response.status_code, 302)
        self.wish.refresh_from_db()
        self.assertFalse(self.wish.is_approved)

    def test_wish_delete_dashboard_view(self):
        """Test deleting a wish submission via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:wish_delete", kwargs={"pk": self.wish.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WishSubmission.objects.filter(pk=self.wish.pk).exists())


class WishSubmissionPublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = BirthdayProfile.objects.create(
            full_name="Simran Kapoor",
            slug="simran",
            birthday_date=date(1999, 5, 20),
            is_active=True
        )
        self.wish = WishSubmission.objects.create(
            birthday_profile=self.profile,
            sender_name="Tanya",
            message="Have a blast!",
            is_approved=True
        )

    def test_public_wish_page_get(self):
        """Test accessing /simran/wish/ loads public make-a-wish page."""
        response = self.client.get("/simran/wish/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wishes/index.html")
        self.assertContains(response, "Tanya")
        self.assertEqual(response.context["current_step"], 9)
        self.assertEqual(response.context["prev_url"], "/simran/secret/")

    def test_ajax_wish_submission_success(self):
        """Test submitting a new wish via AJAX."""
        response = self.client.post(
            "/simran/wish/",
            {
                "sender_name": "Dev",
                "message": "Many many happy returns of the day!",
                "candle_blown": "true"
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["sender_name"], "Dev")
        self.assertTrue(WishSubmission.objects.filter(sender_name="Dev", candle_blown=True).exists())
