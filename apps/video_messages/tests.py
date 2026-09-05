from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.profiles.models import BirthdayProfile
from apps.video_messages.models import VideoMessage


class VideoMessageModelTest(TestCase):
    def setUp(self):
        self.profile = BirthdayProfile.objects.create(
            full_name="Ishan Malhotra",
            slug="ishan",
            birthday_date=date(1995, 7, 25)
        )
        self.video = VideoMessage.objects.create(
            birthday_profile=self.profile,
            sender_name="Mom & Dad",
            relationship="Parents",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            message_text="Happy Birthday son!",
            display_order=1
        )

    def test_video_message_creation_and_embed_url(self):
        """Test video message creation and embed_url conversion."""
        self.assertEqual(self.video.sender_name, "Mom & Dad")
        self.assertIn("Mom & Dad", str(self.video))
        self.assertEqual(self.video.embed_url, "https://www.youtube.com/embed/dQw4w9WgXcQ")

    def test_vimeo_embed_url(self):
        """Test Vimeo URL conversion to embed format."""
        vimeo_video = VideoMessage.objects.create(
            birthday_profile=self.profile,
            sender_name="Bestie Rahul",
            video_url="https://vimeo.com/123456789"
        )
        self.assertEqual(vimeo_video.embed_url, "https://player.vimeo.com/video/123456789")

    def test_profile_cascade_deletion(self):
        """Test deleting profile automatically deletes associated video messages."""
        profile_pk = self.profile.pk
        video_pk = self.video.pk

        self.profile.delete()

        self.assertFalse(BirthdayProfile.objects.filter(pk=profile_pk).exists())
        self.assertFalse(VideoMessage.objects.filter(pk=video_pk).exists())


class VideoMessageDashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")
        self.profile = BirthdayProfile.objects.create(
            full_name="Nisha Gill",
            slug="nisha",
            birthday_date=date(1997, 3, 30)
        )
        self.video = VideoMessage.objects.create(
            birthday_profile=self.profile,
            sender_name="Aunt Suman",
            relationship="Aunt",
            video_url="https://www.youtube.com/watch?v=abcd12345",
            display_order=1
        )

    def test_video_list_dashboard_view(self):
        """Test dashboard video messages list view."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:video_list", kwargs={"profile_id": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aunt Suman")

    def test_video_create_dashboard_view(self):
        """Test creating a video message via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:video_create", kwargs={"profile_id": self.profile.pk}), {
            "sender_name": "Uncle Raj",
            "relationship": "Uncle",
            "video_url": "https://www.youtube.com/watch?v=xyz987",
            "message_text": "Lots of blessings!",
            "display_order": 2
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(VideoMessage.objects.filter(sender_name="Uncle Raj").exists())

    def test_video_edit_dashboard_view(self):
        """Test editing a video message via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:video_edit", kwargs={"pk": self.video.pk}), {
            "sender_name": "Aunt Suman Updated",
            "relationship": "Aunt",
            "video_url": "https://www.youtube.com/watch?v=abcd12345",
            "display_order": 1
        })
        self.assertEqual(response.status_code, 302)
        self.video.refresh_from_db()
        self.assertEqual(self.video.sender_name, "Aunt Suman Updated")

    def test_video_delete_dashboard_view(self):
        """Test deleting a video message via dashboard confirmation."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:video_delete", kwargs={"pk": self.video.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(VideoMessage.objects.filter(pk=self.video.pk).exists())


class VideoMessagePublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = BirthdayProfile.objects.create(
            full_name="Nisha Gill",
            slug="nisha",
            birthday_date=date(1997, 3, 30),
            is_active=True
        )
        self.video = VideoMessage.objects.create(
            birthday_profile=self.profile,
            sender_name="College Gang",
            relationship="Friends",
            video_url="https://www.youtube.com/watch?v=abcd12345"
        )

    def test_public_video_messages_view_success(self):
        """Test accessing /nisha/messages/ loads public video messages page."""
        response = self.client.get("/nisha/messages/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "video_messages/index.html")
        self.assertContains(response, "College Gang")
        self.assertEqual(response.context["current_step"], 8)
        self.assertEqual(response.context["prev_url"], "/nisha/music/")
        self.assertEqual(response.context["next_url"], "/nisha/secret/")
