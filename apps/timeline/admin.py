from django.contrib import admin
from .models import TimelineEvent


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("title", "birthday_profile", "event_date", "icon", "display_order", "created_at")
    list_filter = ("birthday_profile", "event_date")
    search_fields = ("title", "description", "birthday_profile__full_name")
    list_editable = ("display_order",)
