from django.db import models
from django.utils.text import slugify


class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Theme display name")
    slug = models.SlugField(max_length=100, unique=True, help_text="Unique theme identifier")
    primary_color = models.CharField(max_length=30, default="#f43f5e", help_text="Primary brand/accent color")
    secondary_color = models.CharField(max_length=30, default="#f59e0b", help_text="Secondary highlight color")
    background_color = models.CharField(max_length=30, default="#020617", help_text="Page background color")
    text_color = models.CharField(max_length=30, default="#f8fafc", help_text="Primary text color")
    accent_color = models.CharField(max_length=30, default="#fb7185", help_text="Accent color")
    card_bg = models.CharField(max_length=50, default="rgba(255, 255, 255, 0.05)", help_text="Glassmorphic card background")
    card_border = models.CharField(max_length=50, default="rgba(255, 255, 255, 0.1)", help_text="Glassmorphic card border")
    is_default = models.BooleanField(default=False, help_text="Set as platform default theme")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Theme"
        verbose_name_plural = "Themes"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        if self.is_default:
            Theme.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    @property
    def css_variables(self):
        """Generate inline CSS variable definitions for template rendering."""
        return (
            f"--primary-color: {self.primary_color}; "
            f"--secondary-color: {self.secondary_color}; "
            f"--background-color: {self.background_color}; "
            f"--text-color: {self.text_color}; "
            f"--accent-color: {self.accent_color}; "
            f"--card-bg: {self.card_bg}; "
            f"--card-border: {self.card_border};"
        )
