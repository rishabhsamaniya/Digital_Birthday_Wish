from django.db import models


class SecretMessage(models.Model):
    birthday_profile = models.OneToOneField(
        "profiles.BirthdayProfile",
        on_delete=models.CASCADE,
        related_name="secret_message",
        help_text="The birthday profile this secret message belongs to"
    )
    title = models.CharField(
        max_length=200,
        default="A Special Secret Message 🔒",
        help_text="Title or envelope heading for the secret message"
    )
    secret_text = models.TextField(help_text="The confidential, heartfelt secret message text")
    pin_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Optional passcode PIN required to unlock this secret (e.g. '1234', '0415')"
    )
    hint = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional hint to remind the recipient of the PIN (e.g. 'Our anniversary date')"
    )
    image = models.ImageField(
        upload_to="secret/images/",
        blank=True,
        null=True,
        help_text="Optional secret photo or surprise image"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Secret Message"
        verbose_name_plural = "Secret Messages"

    def __str__(self):
        return f"Secret Message for {self.birthday_profile.full_name}"

    def check_pin(self, entered_pin):
        """Verifies if the entered PIN matches the secret message passcode."""
        if not self.pin_code:
            return True
        return str(self.pin_code).strip() == str(entered_pin).strip()
