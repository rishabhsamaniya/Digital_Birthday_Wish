from django.shortcuts import render
from apps.profiles.views import _get_live_profile_or_render
from apps.themes.models import Theme


def memory_stories(request, slug):
    """Step 3: Our Memories public journey page displaying isolated profile memories."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    memories = profile.memories.all()
    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    context = {
        "profile": profile,
        "memories": memories,
        "theme": theme,
        "current_step": 4,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/countdown/",
        "next_url": f"/{profile.slug}/timeline/",

    }
    return render(request, "memories/index.html", context)
