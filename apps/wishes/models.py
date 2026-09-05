from django.db import models


class WishSubmission(models.Model):
    birthday_profile = models.ForeignKey(
        "profiles.BirthdayProfile",
        on_delete=models.CASCADE,
        related_name="wishes",
        help_text="The birthday profile this wish belongs to"
    )
    sender_name = models.CharField(max_length=200, help_text="Name of the person submitting the birthday wish")
    message = models.TextField(help_text="Warm birthday wish message")
    candle_blown = models.BooleanField(default=False, help_text="Whether candle blow animation was triggered")
    is_approved = models.BooleanField(default=True, help_text="Approval status for public wall")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Wish Submission"
        verbose_name_plural = "Wish Submissions"

    def __str__(self):
        return f"Wish from {self.sender_name} for {self.birthday_profile.full_name}"
