from django.contrib import admin
from .models import WishSubmission


@admin.register(WishSubmission)
class WishSubmissionAdmin(admin.ModelAdmin):
    list_display = ("sender_name", "birthday_profile", "candle_blown", "is_approved", "created_at")
    list_filter = ("is_approved", "candle_blown", "created_at")
    search_fields = ("sender_name", "message", "birthday_profile__full_name")
    list_editable = ("is_approved",)
