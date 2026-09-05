from django.contrib import admin
from .models import LoveNote


@admin.register(LoveNote)
class LoveNoteAdmin(admin.ModelAdmin):
    list_display = ("title", "birthday_profile", "icon", "display_order", "created_at")
    list_filter = ("birthday_profile", "created_at")
    search_fields = ("title", "message", "birthday_profile__full_name")
    list_editable = ("display_order",)
