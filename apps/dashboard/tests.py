from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.profiles.models import BirthdayProfile


class DashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpassword123"
        )

        # Create test birthday profile
        self.profile = BirthdayProfile.objects.create(
            full_name="Ananya Roy",
            slug="ananya-roy",
            birthday_date=date(1997, 6, 20),
            is_active=True
        )

    def test_unauthenticated_dashboard_access_redirects(self):
        """Test unauthenticated user is redirected to login page."""
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("dashboard:login"), response.url)

    def test_dashboard_login_success(self):
        """Test login with valid credentials opens dashboard."""
        response = self.client.post(reverse("dashboard:login"), {
            "username": "admin",
            "password": "adminpassword123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard:index"))

    def test_authenticated_dashboard_overview(self):
        """Test logged-in admin can view dashboard overview with metrics."""
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Overview")
        self.assertEqual(response.context["total_profiles"], 1)

    def test_profile_list_view(self):
        """Test listing profiles in dashboard."""
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.get(reverse("dashboard:profile_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ananya Roy")

    def test_profile_create_view(self):
        """Test creating a profile via dashboard form."""
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.post(reverse("dashboard:profile_create"), {
            "full_name": "Rohan Das",
            "nickname": "Ro",
            "slug": "rohan-das",
            "birthday_date": "2000-03-15",
            "is_active": True,
            "enable_animations": True,
            "expiry_behavior": BirthdayProfile.EXPIRY_KEEP_PUBLIC
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BirthdayProfile.objects.filter(slug="rohan-das").exists())

    def test_profile_edit_view(self):
        """Test updating a profile via dashboard form."""
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.post(reverse("dashboard:profile_edit", kwargs={"pk": self.profile.pk}), {
            "full_name": "Ananya Roy Updated",
            "nickname": "Anu",
            "slug": "ananya-roy",
            "birthday_date": "1997-06-20",
            "is_active": True,
            "enable_animations": True,
            "expiry_behavior": BirthdayProfile.EXPIRY_KEEP_PUBLIC
        })
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.full_name, "Ananya Roy Updated")

    def test_profile_toggle_status_view(self):
        """Test toggling active status on a profile."""
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.get(reverse("dashboard:profile_toggle_status", kwargs={"pk": self.profile.pk}))
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_active)

    def test_profile_delete_view(self):
        """Test deleting a profile via dashboard confirmation."""
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.post(reverse("dashboard:profile_delete", kwargs={"pk": self.profile.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BirthdayProfile.objects.filter(pk=self.profile.pk).exists())
