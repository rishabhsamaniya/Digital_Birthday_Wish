from django.contrib import admin
from .models import SecretMessage


@admin.register(SecretMessage)
class SecretMessageAdmin(admin.ModelAdmin):
    list_display = ("birthday_profile", "title", "pin_code", "hint", "created_at")
    search_fields = ("title", "secret_text", "hint", "birthday_profile__full_name")
