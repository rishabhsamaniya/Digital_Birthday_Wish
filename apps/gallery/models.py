from django.db import models


class GalleryPhoto(models.Model):
    birthday_profile = models.ForeignKey(
        "profiles.BirthdayProfile",
        on_delete=models.CASCADE,
        related_name="photos",
        help_text="The birthday profile this gallery photo belongs to"
    )
    title = models.CharField(max_length=200, blank=True, help_text="Optional photo title")
    caption = models.TextField(blank=True, help_text="Optional caption or memory story behind the photo")
    image = models.ImageField(
        upload_to="gallery/images/",
        help_text="Gallery photo image"
    )
    display_order = models.PositiveIntegerField(default=0, help_text="Sort order")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"

    def __str__(self):
        title_str = self.title or f"Photo #{self.pk}"
        return f"{title_str} ({self.birthday_profile.full_name})"
