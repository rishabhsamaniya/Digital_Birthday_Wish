from django.shortcuts import render
from apps.profiles.views import _get_live_profile_or_render
from apps.themes.models import Theme


def gallery_showcase(request, slug):
    """Step 6: Photo Gallery showcase page with Lightbox modal."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    photos = profile.photos.all()
    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    context = {
        "profile": profile,
        "photos": photos,
        "theme": theme,
        "current_step": 6,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/love-notes/",
        "next_url": f"/{profile.slug}/music/",
    }
    return render(request, "gallery/index.html", context)
