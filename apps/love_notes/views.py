from django.shortcuts import render
from apps.profiles.views import _get_live_profile_or_render
from apps.themes.models import Theme


def love_notes_journey(request, slug):
    """Step 5: Things I Love About You public love notes page."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    love_notes = profile.love_notes.all()
    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    context = {
        "profile": profile,
        "love_notes": love_notes,
        "theme": theme,
        "current_step": 5,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/timeline/",
        "next_url": f"/{profile.slug}/gallery/",
    }
    return render(request, "love_notes/index.html", context)
