from django.db import models


class BackgroundMusic(models.Model):
    birthday_profile = models.ForeignKey(
        "profiles.BirthdayProfile",
        on_delete=models.CASCADE,
        related_name="music_tracks",
        help_text="The birthday profile this background music belongs to"
    )
    title = models.CharField(max_length=200, help_text="Song or playlist track title")
    artist = models.CharField(max_length=200, blank=True, help_text="Artist or composer name")
    audio_file = models.FileField(
        upload_to="music/audio/",
        blank=True,
        null=True,
        help_text="Audio file upload (MP3, WAV, OGG, AAC)"
    )
    external_url = models.URLField(
        blank=True,
        help_text="Direct stream URL if not uploading a file"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Primary background track for auto-play across journey steps"
    )
    display_order = models.PositiveIntegerField(default=0, help_text="Sort order")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_primary", "display_order", "-created_at"]
        verbose_name = "Background Music Track"
        verbose_name_plural = "Background Music Tracks"

    def __str__(self):
        artist_str = f" - {self.artist}" if self.artist else ""
        return f"{self.title}{artist_str} ({self.birthday_profile.full_name})"

    @property
    def audio_url(self):
        if self.audio_file:
            return self.audio_file.url
        return self.external_url or ""
