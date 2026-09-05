from django.contrib import admin
from .models import BackgroundMusic


@admin.register(BackgroundMusic)
class BackgroundMusicAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "birthday_profile", "is_primary", "display_order", "created_at")
    list_filter = ("birthday_profile", "is_primary", "created_at")
    search_fields = ("title", "artist", "birthday_profile__full_name")
    list_editable = ("is_primary", "display_order")
