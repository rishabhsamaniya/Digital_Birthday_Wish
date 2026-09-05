from django.db import models


class Memory(models.Model):
    birthday_profile = models.ForeignKey(
        "profiles.BirthdayProfile",
        on_delete=models.CASCADE,
        related_name="memories",
        help_text="The birthday profile this memory belongs to"
    )
    title = models.CharField(max_length=200, help_text="Title or caption for the memory")
    description = models.TextField(help_text="Detailed story or recollection")
    memory_date = models.DateField(blank=True, null=True, help_text="Date this memory took place")
    image = models.ImageField(
        upload_to="memories/images/",
        blank=True,
        null=True,
        help_text="Photo associated with this memory"
    )
    display_order = models.PositiveIntegerField(default=0, help_text="Order in which memory is displayed")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "memory_date", "-created_at"]
        verbose_name = "Memory"
        verbose_name_plural = "Memories"

    def __str__(self):
        return f"{self.title} ({self.birthday_profile.full_name})"
