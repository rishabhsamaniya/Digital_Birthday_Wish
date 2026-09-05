from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.profiles.models import BirthdayProfile
from apps.gallery.models import GalleryPhoto

# Valid 1x1 pixel GIF image bytes
VALID_GIF_BYTES = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff"
    b"\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00"
    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


class GalleryModelTest(TestCase):
    def setUp(self):
        self.profile = BirthdayProfile.objects.create(
            full_name="Tara Sengupta",
            slug="tara",
            birthday_date=date(1997, 10, 12)
        )
        self.dummy_image = SimpleUploadedFile("test.gif", VALID_GIF_BYTES, content_type="image/gif")
        self.photo = GalleryPhoto.objects.create(
            birthday_profile=self.profile,
            title="Golden Hour",
            caption="Taken during our evening walk.",
            image=self.dummy_image,
            display_order=1
        )

    def test_gallery_photo_creation_and_string(self):
        """Test gallery photo creation and string representation."""
        self.assertEqual(self.photo.title, "Golden Hour")
        self.assertIn("Golden Hour", str(self.photo))
        self.assertEqual(self.photo.birthday_profile, self.profile)

    def test_profile_cascade_deletion(self):
        """Test deleting profile automatically deletes associated gallery photos."""
        profile_pk = self.profile.pk
        photo_pk = self.photo.pk

        self.profile.delete()

        self.assertFalse(BirthdayProfile.objects.filter(pk=profile_pk).exists())
        self.assertFalse(GalleryPhoto.objects.filter(pk=photo_pk).exists())


class GalleryDashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")
        self.profile = BirthdayProfile.objects.create(
            full_name="Kabir Joshi",
            slug="kabir",
            birthday_date=date(1993, 4, 18)
        )
        self.dummy_image = SimpleUploadedFile("test.gif", VALID_GIF_BYTES, content_type="image/gif")
        self.photo = GalleryPhoto.objects.create(
            birthday_profile=self.profile,
            title="Mountain Hike",
            caption="Conquered the peak together.",
            image=self.dummy_image,
            display_order=1
        )

    def test_gallery_list_dashboard_view(self):
        """Test dashboard gallery photo list view."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:gallery_list", kwargs={"profile_id": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mountain Hike")

    def test_gallery_create_dashboard_view(self):
        """Test creating a new gallery photo via dashboard."""
        self.client.login(username="admin", password="password123")
        new_image = SimpleUploadedFile("new.gif", VALID_GIF_BYTES, content_type="image/gif")
        response = self.client.post(reverse("dashboard:gallery_create", kwargs={"profile_id": self.profile.pk}), {
            "title": "Sunset View",
            "caption": "Beautiful sunset.",
            "image": new_image,
            "display_order": 2
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(GalleryPhoto.objects.filter(title="Sunset View").exists())

    def test_gallery_edit_dashboard_view(self):
        """Test editing a gallery photo via dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:gallery_edit", kwargs={"pk": self.photo.pk}), {
            "title": "Mountain Hike Updated",
            "caption": "Updated caption.",
            "display_order": 1
        })
        self.assertEqual(response.status_code, 302)
        self.photo.refresh_from_db()
        self.assertEqual(self.photo.title, "Mountain Hike Updated")

    def test_gallery_delete_dashboard_view(self):
        """Test deleting a gallery photo via dashboard confirmation."""
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse("dashboard:gallery_delete", kwargs={"pk": self.photo.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(GalleryPhoto.objects.filter(pk=self.photo.pk).exists())


class GalleryPublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = BirthdayProfile.objects.create(
            full_name="Kabir Joshi",
            slug="kabir",
            birthday_date=date(1993, 4, 18),
            is_active=True
        )
        self.dummy_image = SimpleUploadedFile("test.gif", VALID_GIF_BYTES, content_type="image/gif")
        self.photo = GalleryPhoto.objects.create(
            birthday_profile=self.profile,
            title="City Lights",
            caption="Stargazing in the city.",
            image=self.dummy_image,
            display_order=1
        )

    def test_public_gallery_view_success(self):
        """Test accessing /kabir/gallery/ loads public gallery page."""
        response = self.client.get("/kabir/gallery/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gallery/index.html")
        self.assertContains(response, "City Lights")
        self.assertEqual(response.context["current_step"], 6)
        self.assertEqual(response.context["prev_url"], "/kabir/love-notes/")
        self.assertEqual(response.context["next_url"], "/kabir/music/")
