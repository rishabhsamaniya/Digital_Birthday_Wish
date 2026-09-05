from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.profiles.models import BirthdayProfile
from apps.timeline.models import TimelineEvent


class TimelineModelTest(TestCase):
    def setUp(self):
        self.profile = BirthdayProfile.objects.create(
            full_name="Vikram Singh",
            slug="vikram",
            birthday_date=date(1995, 3, 10)
        )
        self.event1 = TimelineEvent.objects.create(
            birthday_profile=self.profile,
            title="First Day We Met",
            description="Met at campus library.",
            event_date=date(2018, 9, 1),
            display_order=1
        )
        self.event2 = TimelineEvent.objects.create(
            birthday_profile=self.profile,
            title="Graduation Day",
            description="Celebrated our graduation together.",
            event_date=date(2021, 6, 15),
            display_order=2
        )

    def test_timeline_event_creation_and_string(self):
        """Test timeline event creation and string representation."""
        self.assertEqual(self.event1.title, "First Day We Met")
        self.assertIn("First Day We Met", str(self.event1))
        self.assertEqual(self.event1.birthday_profile, self.profile)

    def test_profile_cascade_deletion(self):
        """Test deleting profile automatically deletes associated timeline events."""
        profile_pk = self.profile.pk
        event_pk = self.event1.pk

        self.profile.delete()

        self.assertFalse(BirthdayProfile.objects.filter(pk=profile_pk).exists())
        self.assertFalse(TimelineEvent.objects.filter(pk=event_pk).exists())


class TimelineDashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")
        self.profile = BirthdayProfile.objects.create(
            full_name="Meera Kapur",
            slug="meera",
            birthday_date=date(1999, 11, 5)
        )
        self.event = TimelineEvent.objects.create(
            birthday_profile=self.profile,
            title="Road Trip to Goa",
            description="Awesome road trip with friends.",
            event_date=date(2022, 1, 15)
        )

    def test_timeline_list_dashboard_view(self):
        """Test dashboard timeline events list view."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:timeline_list", kwargs={"profile_id": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Road Trip to Goa")

    def test_timeline_create_dashboard_view(self):
        """Test adding timeline event via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:timeline_create", kwargs={"profile_id": self.profile.pk}), {
            "title": "Engagement Day",
            "description": "Exchanged rings.",
            "event_date": "2023-04-10",
            "icon": "💍",
            "display_order": 1
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TimelineEvent.objects.filter(title="Engagement Day").exists())

    def test_timeline_edit_dashboard_view(self):
        """Test editing timeline event via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:timeline_edit", kwargs={"pk": self.event.pk}), {
            "title": "Road Trip to Goa Updated",
            "description": "Updated road trip details.",
            "event_date": "2022-01-15",
            "icon": "🚗",
            "display_order": 1
        })
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Road Trip to Goa Updated")

    def test_timeline_delete_dashboard_view(self):
        """Test deleting timeline event via dashboard confirmation."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:timeline_delete", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TimelineEvent.objects.filter(pk=self.event.pk).exists())


class TimelinePublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = BirthdayProfile.objects.create(
            full_name="Meera Kapur",
            slug="meera",
            birthday_date=date(1999, 11, 5),
            is_active=True
        )
        self.event = TimelineEvent.objects.create(
            birthday_profile=self.profile,
            title="First Concert",
            description="Enjoyed live music.",
            event_date=date(2022, 5, 20)
        )

    def test_public_timeline_view_success(self):
        """Test accessing /meera/timeline/ loads public timeline journey page."""
        response = self.client.get("/meera/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "timeline/index.html")
        self.assertContains(response, "First Concert")
        self.assertEqual(response.context["current_step"], 4)
        self.assertEqual(response.context["prev_url"], "/meera/memories/")
        self.assertEqual(response.context["next_url"], "/meera/love-notes/")
