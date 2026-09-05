import re
from django.db import models


class VideoMessage(models.Model):
    birthday_profile = models.ForeignKey(
        "profiles.BirthdayProfile",
        on_delete=models.CASCADE,
        related_name="video_messages",
        help_text="The birthday profile this video message belongs to"
    )
    sender_name = models.CharField(max_length=200, help_text="Name of sender e.g., 'Mom & Dad', 'Bestie Rahul'")
    relationship = models.CharField(max_length=100, blank=True, help_text="e.g. 'Parents', 'College Friend'")
    video_file = models.FileField(
        upload_to="videos/",
        blank=True,
        null=True,
        help_text="Direct video file upload (MP4, WebM)"
    )
    video_url = models.URLField(
        blank=True,
        help_text="YouTube, Vimeo, or direct video stream URL"
    )
    thumbnail = models.ImageField(
        upload_to="videos/thumbnails/",
        blank=True,
        null=True,
        help_text="Optional video thumbnail cover image"
    )
    message_text = models.TextField(blank=True, help_text="Optional text caption accompanying video")
    display_order = models.PositiveIntegerField(default=0, help_text="Sort order")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Video Message"
        verbose_name_plural = "Video Messages"

    def __str__(self):
        return f"Video from {self.sender_name} ({self.birthday_profile.full_name})"

    @property
    def embed_url(self):
        """Converts standard YouTube / Vimeo URLs to embeddable player iframe URLs."""
        if not self.video_url:
            return ""

        yt_match = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)", self.video_url)
        if yt_match:
            return f"https://www.youtube.com/embed/{yt_match.group(1)}"

        vimeo_match = re.search(r"vimeo\.com/(\d+)", self.video_url)
        if vimeo_match:
            return f"https://player.vimeo.com/video/{vimeo_match.group(1)}"

        return self.video_url
