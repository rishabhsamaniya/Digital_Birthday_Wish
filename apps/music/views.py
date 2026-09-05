from django.shortcuts import render
from apps.profiles.views import _get_live_profile_or_render
from apps.themes.models import Theme


def music_experience(request, slug):
    """Step 7: Music Player public journey page."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    music_tracks = profile.music_tracks.all()
    primary_track = music_tracks.filter(is_primary=True).first() or music_tracks.first()
    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    context = {
        "profile": profile,
        "music_tracks": music_tracks,
        "primary_track": primary_track,
        "theme": theme,
        "current_step": 7,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/gallery/",
        "next_url": f"/{profile.slug}/messages/",
    }
    return render(request, "music/index.html", context)
