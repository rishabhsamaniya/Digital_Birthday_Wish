from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.profiles.models import BirthdayProfile
from apps.memories.models import Memory


class MemoryModelTest(TestCase):
    def setUp(self):
        self.profile = BirthdayProfile.objects.create(
            full_name="Ananya Sharma",
            slug="ananya",
            birthday_date=date(1998, 4, 15)
        )
        self.memory = Memory.objects.create(
            birthday_profile=self.profile,
            title="Our First Coffee Date",
            description="We met at the corner cafe and talked for hours.",
            memory_date=date(2020, 2, 14),
            display_order=1
        )

    def test_memory_creation_and_string(self):
        """Test memory creation and string representation."""
        self.assertEqual(self.memory.title, "Our First Coffee Date")
        self.assertEqual(str(self.memory), "Our First Coffee Date (Ananya Sharma)")
        self.assertEqual(self.memory.birthday_profile, self.profile)

    def test_profile_cascade_deletion(self):
        """Test deleting profile automatically deletes associated memories."""
        profile_pk = self.profile.pk
        memory_pk = self.memory.pk

        self.profile.delete()

        self.assertFalse(BirthdayProfile.objects.filter(pk=profile_pk).exists())
        self.assertFalse(Memory.objects.filter(pk=memory_pk).exists())


class MemoryDashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")
        self.profile = BirthdayProfile.objects.create(
            full_name="Priya Patel",
            slug="priya-patel",
            birthday_date=date(1996, 9, 10)
        )
        self.memory = Memory.objects.create(
            birthday_profile=self.profile,
            title="Beach Sunset Walk",
            description="Walking along the shore during sunset.",
            memory_date=date(2021, 5, 20)
        )

    def test_memory_list_view(self):
        """Test viewing memories for a profile in dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:memory_list", kwargs={"profile_id": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Beach Sunset Walk")

    def test_memory_create_view(self):
        """Test adding a new memory via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:memory_create", kwargs={"profile_id": self.profile.pk}), {
            "title": "Surprise Dinner",
            "description": "Candlelight dinner under the stars.",
            "memory_date": "2022-08-15",
            "display_order": 2
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Memory.objects.filter(title="Surprise Dinner").exists())

    def test_memory_edit_view(self):
        """Test editing a memory via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:memory_edit", kwargs={"pk": self.memory.pk}), {
            "title": "Beach Sunset Walk Updated",
            "description": "Updated description.",
            "memory_date": "2021-05-20",
            "display_order": 1
        })
        self.assertEqual(response.status_code, 302)
        self.memory.refresh_from_db()
        self.assertEqual(self.memory.title, "Beach Sunset Walk Updated")

    def test_memory_delete_view(self):
        """Test deleting a memory via dashboard confirmation."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:memory_delete", kwargs={"pk": self.memory.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Memory.objects.filter(pk=self.memory.pk).exists())


class MemoryFrontendViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = BirthdayProfile.objects.create(
            full_name="Sneha Verma",
            slug="sneha",
            birthday_date=date(1999, 3, 25),
            is_active=True
        )
        self.memory = Memory.objects.create(
            birthday_profile=self.profile,
            title="First Trip Together",
            description="We travelled to the mountains.",
            display_order=1
        )

    def test_memory_stories_public_view_success(self):
        """Test accessing /sneha/memories/ loads public memory stories page."""
        response = self.client.get("/sneha/memories/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memories/index.html")
        self.assertContains(response, "First Trip Together")
        self.assertEqual(response.context["current_step"], 4)
        self.assertEqual(response.context["prev_url"], "/sneha/countdown/")
        self.assertEqual(response.context["next_url"], "/sneha/timeline/")

