from datetime import date, timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from apps.profiles.models import BirthdayProfile
from apps.themes.models import Theme
from apps.profiles.services.qr_service import generate_qr_code_image


class BirthdayProfileModelTest(TestCase):
    def setUp(self):
        self.profile = BirthdayProfile.objects.create(
            full_name="Priya Sharma",
            nickname="Pree",
            slug="priya",
            birthday_date=date(1998, 5, 15),
            intro_message="Welcome Priya!",
            final_message="Happy Birthday Priya!"
        )

    def test_profile_creation(self):
        """Test basic creation and string representation of BirthdayProfile."""
        self.assertEqual(self.profile.full_name, "Priya Sharma")
        self.assertEqual(self.profile.slug, "priya")
        self.assertEqual(str(self.profile), "Priya Sharma (priya)")
        self.assertTrue(self.profile.is_active)
        self.assertTrue(self.profile.enable_animations)

    def test_unique_slug_enforcement(self):
        """Test duplicate slug raises ValidationError."""
        duplicate = BirthdayProfile(
            full_name="Priya Patel",
            slug="priya",
            birthday_date=date(1995, 10, 20)
        )
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_reserved_slug_validation(self):
        """Test reserved slugs raise ValidationError."""
        reserved_profile = BirthdayProfile(
            full_name="Admin User",
            slug="admin",
            birthday_date=date(2000, 1, 1)
        )
        with self.assertRaises(ValidationError):
            reserved_profile.full_clean()

    def test_auto_slug_generation(self):
        """Test slug is automatically generated if omitted."""
        new_profile = BirthdayProfile.objects.create(
            full_name="Sneha Roy",
            birthday_date=date(1997, 8, 12)
        )
        self.assertEqual(new_profile.slug, "sneha-roy")

    def test_is_currently_live_active_profile(self):
        """Test live property returns True for active profile without dates."""
        self.assertTrue(self.profile.is_currently_live)

    def test_is_currently_live_inactive_profile(self):
        """Test live property returns False when is_active is False."""
        self.profile.is_active = False
        self.profile.save()
        self.assertFalse(self.profile.is_currently_live)

    def test_is_currently_live_scheduled_future_publish(self):
        """Test profile scheduled in future is not live."""
        future_time = timezone.now() + timedelta(days=2)
        self.profile.publish_date = future_time
        self.profile.save()
        self.assertFalse(self.profile.is_currently_live)

    def test_is_currently_live_expired_make_private(self):
        """Test expired profile with make_private behavior is not live."""
        past_time = timezone.now() - timedelta(days=2)
        self.profile.expiry_date = past_time
        self.profile.expiry_behavior = BirthdayProfile.EXPIRY_MAKE_PRIVATE
        self.profile.save()
        self.assertFalse(self.profile.is_currently_live)

    def test_is_currently_live_expired_keep_public(self):
        """Test expired profile with keep_public behavior remains live."""
        past_time = timezone.now() - timedelta(days=2)
        self.profile.expiry_date = past_time
        self.profile.expiry_behavior = BirthdayProfile.EXPIRY_KEEP_PUBLIC
        self.profile.save()
        self.assertTrue(self.profile.is_currently_live)


class BirthdayProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.theme = Theme.objects.get(slug="luxury-dark")

        self.profile = BirthdayProfile.objects.create(
            full_name="Sneha Verma",
            slug="sneha",
            birthday_date=date(1999, 3, 25),
            theme=self.theme,
            is_active=True
        )

        self.inactive_profile = BirthdayProfile.objects.create(
            full_name="Rahul Mehra",
            slug="rahul",
            birthday_date=date(1995, 1, 10),
            is_active=False
        )

        self.scheduled_profile = BirthdayProfile.objects.create(
            full_name="Ananya Sharma",
            slug="ananya",
            birthday_date=date(2001, 7, 4),
            publish_date=timezone.now() + timedelta(days=5),
            is_active=True
        )

        self.expired_private_profile = BirthdayProfile.objects.create(
            full_name="Vikram Seth",
            slug="vikram",
            birthday_date=date(1992, 11, 18),
            expiry_date=timezone.now() - timedelta(days=1),
            expiry_behavior=BirthdayProfile.EXPIRY_MAKE_PRIVATE,
            is_active=True
        )

    def test_valid_profile_url_returns_200(self):
        """Test accessing /sneha/ loads landing page successfully."""
        response = self.client.get("/sneha/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sneha Verma")
        self.assertTemplateUsed(response, "profiles/landing.html")

    def test_nonexistent_profile_returns_404(self):
        """Test accessing non-existent slug returns 404."""
        response = self.client.get("/unknown-slug/")
        self.assertEqual(response.status_code, 404)

    def test_inactive_profile_returns_403(self):
        """Test accessing inactive profile returns 403 inactive template."""
        response = self.client.get("/rahul/")
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "profiles/inactive.html")

    def test_scheduled_profile_returns_200_scheduled(self):
        """Test accessing scheduled future profile returns pending page."""
        response = self.client.get("/ananya/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/scheduled.html")
        self.assertContains(response, "This surprise isn't ready yet")

    def test_expired_private_profile_returns_403(self):
        """Test accessing expired profile with make_private behavior returns 403."""
        response = self.client.get("/vikram/")
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "profiles/expired.html")

    def test_birthday_reveal_view_success(self):
        """Test accessing /sneha/birthday/ loads birthday reveal page successfully."""
        response = self.client.get("/sneha/birthday/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/birthday_reveal.html")
        self.assertEqual(response.context["current_step"], 2)
        self.assertEqual(response.context["prev_url"], "/sneha/")
        self.assertEqual(response.context["next_url"], "/sneha/countdown/")

    def test_countdown_timer_view_success(self):
        """Test accessing /sneha/countdown/ loads live countdown page successfully."""
        response = self.client.get("/sneha/countdown/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/countdown.html")
        self.assertEqual(response.context["current_step"], 3)
        self.assertEqual(response.context["prev_url"], "/sneha/birthday/")
        self.assertEqual(response.context["next_url"], "/sneha/memories/")

    def test_birthday_card_view_success(self):
        """Test accessing /sneha/card/ loads digital birthday card page successfully."""
        response = self.client.get("/sneha/card/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/card.html")
        self.assertEqual(response.context["current_step"], 9)
        self.assertEqual(response.context["prev_url"], "/sneha/wish/")
        self.assertEqual(response.context["next_url"], "/sneha/")



    def test_public_qr_code_view(self):
        """Test accessing /sneha/qr/ returns PNG image."""
        response = self.client.get("/sneha/qr/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertTrue(len(response.content) > 0)

    def test_create_wizard_unauthenticated_redirects_login(self):
        """Test unauthenticated user accessing /create/ is redirected to login page."""
        response = self.client.get("/create/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_create_wizard_authenticated_success(self):
        """Test logged in user creating profile via wizard."""
        user = User.objects.create_user("creator", "creator@test.com", "pass123")
        self.client.force_login(user)

        data = {
            "full_name": "Rohan Malhotra",
            "nickname": "Rohu",
            "slug": "rohan",
            "birthday_date": "1999-10-10",
            "intro_message": "Welcome to Rohan's Birthday Party!",
            "final_message": "Happy Birthday Rohan!",
            "secret_text": "Surprise concert tickets!",
            "pin_code": "4321",
        }
        response = self.client.post("/create/", data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BirthdayProfile.objects.filter(slug="rohan", created_by=user).exists())



class QRCodeServiceTest(TestCase):
    def test_generate_qr_code_image_utility(self):
        """Test QR code generation service returns valid PNG buffer."""
        buffer = generate_qr_code_image("https://example.com/sneha/")
        self.assertIsNotNone(buffer)
        image_bytes = buffer.getvalue()
        self.assertTrue(len(image_bytes) > 0)
        self.assertTrue(image_bytes.startswith(b"\x89PNG"))


class QRCodeDashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")
        self.profile = BirthdayProfile.objects.create(
            full_name="Karan Oberoi",
            slug="karan",
            birthday_date=date(1996, 4, 15)
        )

    def test_dashboard_profile_qr_download(self):
        """Test downloading profile QR code from admin dashboard."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("dashboard:profile_qr", kwargs={"pk": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertIn("attachment;", response["Content-Disposition"])
