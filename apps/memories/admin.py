from django.contrib import admin
from .models import Memory


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ("title", "birthday_profile", "memory_date", "display_order", "created_at")
    list_filter = ("birthday_profile", "memory_date", "created_at")
    search_fields = ("title", "description", "birthday_profile__full_name")
    list_editable = ("display_order",)
