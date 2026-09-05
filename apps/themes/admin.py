from django.contrib import admin
from .models import Theme


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "primary_color",
        "secondary_color",
        "background_color",
        "text_color",
        "accent_color",
        "is_default",
        "created_at",
    )
    list_filter = ("is_default", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        ("Theme Information", {
            "fields": ("name", "slug", "is_default")
        }),
        ("Color Palette", {
            "fields": (
                "primary_color",
                "secondary_color",
                "background_color",
                "text_color",
                "accent_color",
            )
        }),
        ("Card & Container Styles", {
            "fields": (
                "card_bg",
                "card_border",
            )
        }),
    )
