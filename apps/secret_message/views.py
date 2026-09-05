from django.shortcuts import render
from django.http import JsonResponse
from apps.profiles.views import _get_live_profile_or_render
from apps.themes.models import Theme


def secret_message_reveal(request, slug):
    """Step 9: Secret Message public journey page with optional PIN lock screen."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    secret = getattr(profile, "secret_message", None)
    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    # Handle AJAX PIN Verification Request
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        entered_pin = request.POST.get("pin", "")
        if secret and secret.check_pin(entered_pin):
            image_url = secret.image.url if secret.image else None
            return JsonResponse({
                "success": True,
                "title": secret.title,
                "secret_text": secret.secret_text,
                "image_url": image_url
            })
        return JsonResponse({"success": False, "error": "Incorrect passcode PIN. Please try again! 🔒"})

    context = {
        "profile": profile,
        "secret": secret,
        "theme": theme,
        "current_step": 9,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/messages/",
        "next_url": f"/{profile.slug}/wish/",
    }
    return render(request, "secret_message/index.html", context)
