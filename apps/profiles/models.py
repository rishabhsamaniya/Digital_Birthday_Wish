import secrets

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify

RESERVED_SLUGS = ["admin", "dashboard", "static", "media", "api", "login", "logout", "create", "my-wishes", "accounts"]


def validate_reserved_slug(value):
    """Ensure the slug is not a system reserved word."""
    if value.lower() in RESERVED_SLUGS:
        raise ValidationError(
            f"'{value}' is a reserved URL path and cannot be used as a profile slug."
        )


class BirthdayProfile(models.Model):
    EXPIRY_KEEP_PUBLIC = "keep_public"
    EXPIRY_MAKE_PRIVATE = "make_private"

    EXPIRY_BEHAVIOR_CHOICES = [
        (EXPIRY_KEEP_PUBLIC, "Keep Public (Accessible after expiry)"),
        (EXPIRY_MAKE_PRIVATE, "Make Private (Restricted after expiry)"),
    ]

    # Owner / Author Attribution
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="birthday_profiles",
        help_text="User who created this birthday profile"
    )

    # Primary identification
    full_name = models.CharField(max_length=150, help_text="Full name of the birthday person")
    nickname = models.CharField(max_length=100, blank=True, help_text="Sweet nickname or preferred name")
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        validators=[validate_reserved_slug],
        help_text="Unique URL path slug (e.g., 'priya' for /priya/)"
    )


    # Dates
    birthday_date = models.DateField(help_text="The birthday date")
    birth_place = models.CharField(
        max_length=150,
        blank=True,
        help_text="Optional city or place shown on the countdown page"
    )
    relationship_start_date = models.DateField(blank=True, null=True, help_text="Date relationship started")
    first_meeting_date = models.DateField(blank=True, null=True, help_text="Date of first meeting")

    # Images
    profile_image = models.ImageField(
        upload_to="profiles/profile_images/",
        blank=True,
        null=True,
        help_text="Main profile picture"
    )
    hero_image = models.ImageField(
        upload_to="profiles/hero_images/",
        blank=True,
        null=True,
        help_text="Hero section backdrop image"
    )
    cover_image = models.ImageField(
        upload_to="profiles/cover_images/",
        blank=True,
        null=True,
        help_text="Cover banner image"
    )

    # Messages
    intro_message = models.TextField(blank=True, help_text="Landing intro text")
    final_message = models.TextField(blank=True, help_text="Closing birthday message")
    special_letter = models.TextField(blank=True, help_text="Private or special letter message")

    # Status & Publishing Schedule
    is_active = models.BooleanField(default=True, help_text="Master active toggle for the profile")
    publish_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Schedule profile to go live at a specific date/time (optional)"
    )
    expiry_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Optional expiration date/time"
    )
    expiry_behavior = models.CharField(
        max_length=20,
        choices=EXPIRY_BEHAVIOR_CHOICES,
        default=EXPIRY_KEEP_PUBLIC,
        help_text="Action to take when expiry date is reached"
    )

    # Display Preferences & Theme
    theme = models.ForeignKey(
        "themes.Theme",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="profiles",
        help_text="Visual theme for this birthday profile"
    )
    enable_animations = models.BooleanField(
        default=True,
        help_text="Enable floating hearts, confetti, and visual animations"
    )

    # --- Access Password Protection ---
    is_password_protected = models.BooleanField(
        default=True,
        help_text="If True, recipients must enter the access password to view the birthday page"
    )
    access_password_hash = models.CharField(
        max_length=255,
        blank=True,
        help_text="Hashed unique access password shown once to the creator after publish"
    )

    # Payment gate for QR/public journey access
    is_paid = models.BooleanField(default=False, help_text="Whether the creation payment has been verified")
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Birthday Profile"
        verbose_name_plural = "Birthday Profiles"

    def __str__(self):
        return f"{self.full_name} ({self.slug})"

    # ------------------------------------------------------------------
    # Access Password Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def derive_plain_password(full_name: str, birthday_date) -> str:
        """
        Derive the plain-text access password.
        Formula: <first_name_lowercase><birth_year>
        e.g.  full_name="Sneha Sharma", birthday_date=2000-09-15  →  "sneha2000"
        """
        first_name = full_name.strip().split()[0].lower() if full_name.strip() else "user"
        year = birthday_date.year if birthday_date else 2000
        return f"{first_name}{year}"

    def set_access_password(self):
        """Auto-compute and store the hashed access password."""
        from django.contrib.auth.hashers import make_password
        plain = self.derive_plain_password(self.full_name, self.birthday_date)
        self.access_password_hash = make_password(plain)

    def check_access_password(self, entered_password: str) -> bool:
        """Return True if entered_password matches the stored hash."""
        from django.contrib.auth.hashers import check_password
        if not self.access_password_hash:
            return True  # No password set → open access
        return check_password(entered_password, self.access_password_hash)

    @property
    def plain_password_hint(self) -> str:
        """Return the plain-text password for display to the creator (shown once on success page)."""
        return self.derive_plain_password(self.full_name, self.birthday_date)

    # ------------------------------------------------------------------

    def clean(self):
        super().clean()
        if self.slug:
            self.slug = self.slug.lower().strip()
            validate_reserved_slug(self.slug)

        if self.publish_date and self.expiry_date:
            if self.expiry_date <= self.publish_date:
                raise ValidationError({
                    "expiry_date": "Expiry date must be after the publish date."
                })

    def save(self, *args, **kwargs):
        if not self.slug and self.full_name:
            self.slug = slugify(self.full_name)
        self.full_name = self.full_name.strip()
        self.full_clean()
        # Auto-derive and store access password hash on first save or if not set
        if self.is_password_protected and not self.access_password_hash and self.full_name and self.birthday_date:
            self.set_access_password()
        super().save(*args, **kwargs)

    @property
    def is_currently_live(self):
        """Check if profile is active and within scheduled publish/expiry range."""
        if not self.is_active:
            return False

        now = timezone.now()
        if self.publish_date and now < self.publish_date:
            return False

        if self.expiry_date and now > self.expiry_date:
            if self.expiry_behavior == self.EXPIRY_MAKE_PRIVATE:
                return False

        return True

    def get_absolute_url(self):
        return f"/{self.slug}/"
