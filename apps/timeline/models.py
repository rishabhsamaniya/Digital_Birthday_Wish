from django.db import models
from apps.media_utils import optimize_image_field


class TimelineEvent(models.Model):
    birthday_profile = models.ForeignKey(
        "profiles.BirthdayProfile",
        on_delete=models.CASCADE,
        related_name="timeline_events",
        help_text="The birthday profile this timeline event belongs to"
    )
    title = models.CharField(max_length=200, help_text="Event title")
    description = models.TextField(help_text="Story or details about this milestone")
    event_date = models.DateField(help_text="Date this event took place")
    image = models.ImageField(
        upload_to="timeline/images/",
        blank=True,
        null=True,
        help_text="Photo associated with this timeline event"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        default="✨",
        help_text="Emoji or icon identifier (e.g. 💍, ✈️, ☕, 🎂)"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Secondary sort order if multiple events occur on the same date"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["event_date", "display_order", "-created_at"]
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"

    def __str__(self):
        return f"{self.title} ({self.event_date}) - {self.birthday_profile.full_name}"

    def save(self, *args, **kwargs):
        if self.image and not self.image._committed:
            optimize_image_field(self.image)
        super().save(*args, **kwargs)
