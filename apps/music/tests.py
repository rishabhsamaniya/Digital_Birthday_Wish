from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.profiles.models import BirthdayProfile
from apps.music.models import BackgroundMusic


class MusicModelTest(TestCase):
    def setUp(self):
        self.profile = BirthdayProfile.objects.create(
            full_name="Aarav Sharma",
            slug="aarav",
            birthday_date=date(1996, 5, 20)
        )
        self.dummy_audio = SimpleUploadedFile("song.mp3", b"audio_content", content_type="audio/mpeg")
        self.track = BackgroundMusic.objects.create(
            birthday_profile=self.profile,
            title="Golden Memories",
            artist="Acoustic Dreams",
            audio_file=self.dummy_audio,
            is_primary=True,
            display_order=1
        )

    def test_music_creation_and_audio_url(self):
        """Test music track creation and audio_url property."""
        self.assertEqual(self.track.title, "Golden Memories")
        self.assertIn("Golden Memories", str(self.track))
        self.assertTrue(self.track.is_primary)
        self.assertIn("song", self.track.audio_url)

    def test_external_url_fallback(self):
        """Test external_url is returned if audio_file is not attached."""
        external_track = BackgroundMusic.objects.create(
            birthday_profile=self.profile,
            title="External Stream",
            external_url="https://stream.example.com/audio.mp3"
        )
        self.assertEqual(external_track.audio_url, "https://stream.example.com/audio.mp3")

    def test_profile_cascade_deletion(self):
        """Test deleting profile automatically deletes associated music tracks."""
        profile_pk = self.profile.pk
        track_pk = self.track.pk

        self.profile.delete()

        self.assertFalse(BirthdayProfile.objects.filter(pk=profile_pk).exists())
        self.assertFalse(BackgroundMusic.objects.filter(pk=track_pk).exists())


class MusicDashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")
        self.profile = BirthdayProfile.objects.create(
            full_name="Dia Roy",
            slug="dia",
            birthday_date=date(1998, 1, 15)
        )
        self.dummy_audio = SimpleUploadedFile("song.mp3", b"audio_content", content_type="audio/mpeg")
        self.track = BackgroundMusic.objects.create(
            birthday_profile=self.profile,
            title="Birthday Waltz",
            artist="Piano Solos",
            audio_file=self.dummy_audio,
            display_order=1
        )

    def test_music_list_dashboard_view(self):
        """Test dashboard music track list view."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:music_list", kwargs={"profile_id": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Birthday Waltz")

    def test_music_create_dashboard_view(self):
        """Test creating a new music track via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:music_create", kwargs={"profile_id": self.profile.pk}), {
            "title": "Summer Vibes",
            "artist": "DJ Chill",
            "external_url": "https://example.com/vibes.mp3",
            "is_primary": True,
            "display_order": 2
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BackgroundMusic.objects.filter(title="Summer Vibes").exists())

    def test_music_edit_dashboard_view(self):
        """Test editing a music track via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:music_edit", kwargs={"pk": self.track.pk}), {
            "title": "Birthday Waltz Updated",
            "artist": "Piano Solos",
            "external_url": "https://example.com/updated.mp3",
            "display_order": 1
        })
        self.assertEqual(response.status_code, 302)
        self.track.refresh_from_db()
        self.assertEqual(self.track.title, "Birthday Waltz Updated")

    def test_music_delete_dashboard_view(self):
        """Test deleting a music track via dashboard confirmation."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:music_delete", kwargs={"pk": self.track.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BackgroundMusic.objects.filter(pk=self.track.pk).exists())


class MusicPublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = BirthdayProfile.objects.create(
            full_name="Dia Roy",
            slug="dia",
            birthday_date=date(1998, 1, 15),
            is_active=True
        )
        self.track = BackgroundMusic.objects.create(
            birthday_profile=self.profile,
            title="Acoustic Love",
            external_url="https://example.com/acoustic.mp3",
            is_primary=True
        )

    def test_public_music_view_success(self):
        """Test accessing /dia/music/ loads public music player page."""
        response = self.client.get("/dia/music/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "music/index.html")
        self.assertContains(response, "Acoustic Love")
        self.assertEqual(response.context["current_step"], 7)
        self.assertEqual(response.context["prev_url"], "/dia/gallery/")
        self.assertEqual(response.context["next_url"], "/dia/messages/")
