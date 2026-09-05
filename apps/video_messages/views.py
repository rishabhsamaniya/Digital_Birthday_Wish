from django.shortcuts import render
from apps.profiles.views import _get_live_profile_or_render
from apps.themes.models import Theme


def video_messages_showcase(request, slug):
    """Step 8: Video Messages cinema showcase public journey page."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    videos = profile.video_messages.all()
    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    context = {
        "profile": profile,
        "videos": videos,
        "theme": theme,
        "current_step": 8,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/music/",
        "next_url": f"/{profile.slug}/secret/",
    }
    return render(request, "video_messages/index.html", context)
