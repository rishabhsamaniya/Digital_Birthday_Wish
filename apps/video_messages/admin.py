from django.contrib import admin
from .models import VideoMessage


@admin.register(VideoMessage)
class VideoMessageAdmin(admin.ModelAdmin):
    list_display = ("sender_name", "relationship", "birthday_profile", "display_order", "created_at")
    list_filter = ("birthday_profile", "created_at")
    search_fields = ("sender_name", "relationship", "message_text", "birthday_profile__full_name")
    list_editable = ("display_order",)
