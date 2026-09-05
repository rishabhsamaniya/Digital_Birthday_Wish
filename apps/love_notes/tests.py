from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.profiles.models import BirthdayProfile
from apps.love_notes.models import LoveNote


class LoveNoteModelTest(TestCase):
    def setUp(self):
        self.profile = BirthdayProfile.objects.create(
            full_name="Kavya Rao",
            slug="kavya",
            birthday_date=date(1997, 8, 20)
        )
        self.note = LoveNote.objects.create(
            birthday_profile=self.profile,
            title="Your Infectious Smile",
            message="Your smile brightens even the darkest days.",
            icon="💖",
            display_order=1
        )

    def test_love_note_creation_and_string(self):
        """Test love note creation and string representation."""
        self.assertEqual(self.note.title, "Your Infectious Smile")
        self.assertIn("Your Infectious Smile", str(self.note))
        self.assertEqual(self.note.birthday_profile, self.profile)

    def test_profile_cascade_deletion(self):
        """Test deleting profile automatically deletes associated love notes."""
        profile_pk = self.profile.pk
        note_pk = self.note.pk

        self.profile.delete()

        self.assertFalse(BirthdayProfile.objects.filter(pk=profile_pk).exists())
        self.assertFalse(LoveNote.objects.filter(pk=note_pk).exists())


class LoveNoteDashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")
        self.profile = BirthdayProfile.objects.create(
            full_name="Rohan Kapoor",
            slug="rohan",
            birthday_date=date(1994, 12, 1)
        )
        self.note = LoveNote.objects.create(
            birthday_profile=self.profile,
            title="Your Kindness",
            message="Always thinking of others first.",
            icon="🌟",
            display_order=1
        )

    def test_love_note_list_dashboard_view(self):
        """Test dashboard love notes list view."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:love_note_list", kwargs={"profile_id": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Kindness")

    def test_love_note_create_dashboard_view(self):
        """Test adding a love note via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:love_note_create", kwargs={"profile_id": self.profile.pk}), {
            "title": "Your Sense of Humor",
            "message": "Making me laugh uncontrollably.",
            "icon": "😄",
            "display_order": 2
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(LoveNote.objects.filter(title="Your Sense of Humor").exists())

    def test_love_note_edit_dashboard_view(self):
        """Test editing a love note via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:love_note_edit", kwargs={"pk": self.note.pk}), {
            "title": "Your Generous Kindness",
            "message": "Updated message.",
            "icon": "🌟",
            "display_order": 1
        })
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Your Generous Kindness")

    def test_love_note_delete_dashboard_view(self):
        """Test deleting a love note via dashboard confirmation."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:love_note_delete", kwargs={"pk": self.note.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(LoveNote.objects.filter(pk=self.note.pk).exists())


class LoveNotePublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = BirthdayProfile.objects.create(
            full_name="Rohan Kapoor",
            slug="rohan",
            birthday_date=date(1994, 12, 1),
            is_active=True
        )
        self.note = LoveNote.objects.create(
            birthday_profile=self.profile,
            title="Your Warm Hugs",
            message="Feels like home.",
            icon="🤗",
            display_order=1
        )

    def test_public_love_notes_view_success(self):
        """Test accessing /rohan/love-notes/ loads public love notes page."""
        response = self.client.get("/rohan/love-notes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "love_notes/index.html")
        self.assertContains(response, "Your Warm Hugs")
        self.assertEqual(response.context["current_step"], 5)
        self.assertEqual(response.context["prev_url"], "/rohan/timeline/")
        self.assertEqual(response.context["next_url"], "/rohan/gallery/")
