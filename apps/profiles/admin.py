from django.contrib import admin
from .models import BirthdayProfile


@admin.register(BirthdayProfile)
class BirthdayProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "nickname",
        "slug",
        "theme",
        "birthday_date",
        "is_active",
        "is_paid",
        "publish_date",
        "expiry_date",
        "expiry_behavior",
        "created_at",
    )
    list_filter = (
        "theme",
        "is_active",
        "is_paid",
        "expiry_behavior",
        "enable_animations",
        "birthday_date",
        "publish_date",
        "created_at",
    )
    search_fields = ("full_name", "nickname", "slug", "intro_message", "final_message")
    prepopulated_fields = {"slug": ("full_name",)}
    readonly_fields = (
        "created_at",
        "updated_at",
        "razorpay_order_id",
        "razorpay_payment_id",
    )

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "full_name",
                "nickname",
                "slug",
                "birthday_date",
                "relationship_start_date",
                "first_meeting_date",
            )
        }),
        ("Media Assets", {
            "fields": (
                "profile_image",
                "hero_image",
                "cover_image",
            )
        }),
        ("Messages & Content", {
            "fields": (
                "intro_message",
                "final_message",
                "special_letter",
            )
        }),
        ("Publishing & Theme Controls", {
            "fields": (
                "theme",
                "is_active",
                "publish_date",
                "expiry_date",
                "expiry_behavior",
                "enable_animations",
            )
        }),
        ("Payment Status", {
            "fields": (
                "is_paid",
                "razorpay_order_id",
                "razorpay_payment_id",
            )
        }),
        ("System Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )
