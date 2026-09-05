from datetime import date
from django.test import TestCase
from apps.themes.models import Theme
from apps.profiles.models import BirthdayProfile


class ThemeModelTest(TestCase):
    def setUp(self):
        # Fetch or create seeded themes
        self.luxury_dark = Theme.objects.get(slug="luxury-dark")
        self.romantic_red = Theme.objects.get(slug="romantic-red")

    def test_theme_creation_and_string(self):
        """Test theme creation and string representation."""
        self.assertEqual(str(self.luxury_dark), "Luxury Dark")
        self.assertTrue(self.luxury_dark.is_default)
        self.assertFalse(self.romantic_red.is_default)

    def test_css_variables_property(self):
        """Test css_variables property formatting."""
        css_vars = self.luxury_dark.css_variables
        self.assertIn("--primary-color: #d97706;", css_vars)
        self.assertIn("--background-color: #09090b;", css_vars)

    def test_single_default_theme_enforcement(self):
        """Test making romantic_red default clears luxury_dark default status."""
        self.romantic_red.is_default = True
        self.romantic_red.save()

        self.luxury_dark.refresh_from_db()
        self.assertTrue(self.romantic_red.is_default)
        self.assertFalse(self.luxury_dark.is_default)

    def test_profile_theme_association(self):
        """Test associating BirthdayProfile with a Theme."""
        profile = BirthdayProfile.objects.create(
            full_name="Sneha Kapoor",
            slug="sneha-kapoor",
            birthday_date=date(1996, 4, 10),
            theme=self.romantic_red
        )
        self.assertEqual(profile.theme, self.romantic_red)
        self.assertIn(profile, self.romantic_red.profiles.all())
