from django.contrib import admin
from .models import GalleryPhoto


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "birthday_profile", "display_order", "created_at")
    list_filter = ("birthday_profile", "created_at")
    search_fields = ("title", "caption", "birthday_profile__full_name")
    list_editable = ("display_order",)
