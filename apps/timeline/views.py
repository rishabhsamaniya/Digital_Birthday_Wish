from django.shortcuts import render
from apps.profiles.views import _get_live_profile_or_render
from apps.themes.models import Theme


def timeline_journey(request, slug):
    """Step 4: Our Journey dynamic timeline public page."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    timeline_events = profile.timeline_events.all()
    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    context = {
        "profile": profile,
        "timeline_events": timeline_events,
        "theme": theme,
        "current_step": 4,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/memories/",
        "next_url": f"/{profile.slug}/love-notes/",
    }
    return render(request, "timeline/index.html", context)
