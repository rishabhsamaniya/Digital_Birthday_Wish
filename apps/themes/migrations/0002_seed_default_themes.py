from django.db import migrations


def seed_default_themes(apps, schema_editor):
    Theme = apps.get_model("themes", "Theme")
    
    themes = [
        {
            "name": "Luxury Dark",
            "slug": "luxury-dark",
            "primary_color": "#d97706",
            "secondary_color": "#fbbf24",
            "background_color": "#09090b",
            "text_color": "#fafafa",
            "accent_color": "#f59e0b",
            "card_bg": "rgba(255, 255, 255, 0.05)",
            "card_border": "rgba(255, 255, 255, 0.1)",
            "is_default": True,
        },
        {
            "name": "Romantic Red",
            "slug": "romantic-red",
            "primary_color": "#e11d48",
            "secondary_color": "#fda4af",
            "background_color": "#1a050d",
            "text_color": "#fff1f2",
            "accent_color": "#f43f5e",
            "card_bg": "rgba(255, 255, 255, 0.06)",
            "card_border": "rgba(244, 63, 94, 0.2)",
            "is_default": False,
        },
        {
            "name": "Dreamy Pink",
            "slug": "dreamy-pink",
            "primary_color": "#ec4899",
            "secondary_color": "#f472b6",
            "background_color": "#180914",
            "text_color": "#fdf2f8",
            "accent_color": "#f472b6",
            "card_bg": "rgba(255, 255, 255, 0.06)",
            "card_border": "rgba(236, 72, 153, 0.2)",
            "is_default": False,
        },
        {
            "name": "Midnight Love",
            "slug": "midnight-love",
            "primary_color": "#8b5cf6",
            "secondary_color": "#c084fc",
            "background_color": "#050515",
            "text_color": "#f5f3ff",
            "accent_color": "#a855f7",
            "card_bg": "rgba(255, 255, 255, 0.05)",
            "card_border": "rgba(139, 92, 246, 0.2)",
            "is_default": False,
        },
    ]

    for item in themes:
        Theme.objects.get_or_create(slug=item["slug"], defaults=item)


def reverse_seed(apps, schema_editor):
    Theme = apps.get_model("themes", "Theme")
    Theme.objects.filter(slug__in=["luxury-dark", "romantic-red", "dreamy-pink", "midnight-love"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("themes", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_default_themes, reverse_code=reverse_seed),
    ]
