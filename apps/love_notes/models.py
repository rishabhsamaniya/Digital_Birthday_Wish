from django.db import models


class LoveNote(models.Model):
    birthday_profile = models.ForeignKey(
        "profiles.BirthdayProfile",
        on_delete=models.CASCADE,
        related_name="love_notes",
        help_text="The birthday profile this love note belongs to"
    )
    title = models.CharField(max_length=200, help_text="Title or theme of the note (e.g., 'Your Radiant Smile')")
    message = models.TextField(help_text="Personal love note or sweet message")
    icon = models.CharField(
        max_length=50,
        blank=True,
        default="❤️",
        help_text="Emoji or icon identifier (e.g. ❤️, 💖, 🌟, 🌺)"
    )
    display_order = models.PositiveIntegerField(default=0, help_text="Sort order")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Love Note"
        verbose_name_plural = "Love Notes"

    def __str__(self):
        return f"{self.title} ({self.birthday_profile.full_name})"
