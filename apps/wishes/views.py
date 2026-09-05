from django.shortcuts import render
from django.http import JsonResponse
from apps.profiles.views import _get_live_profile_or_render
from apps.themes.models import Theme
from .models import WishSubmission
from .forms import WishSubmissionForm


def wish_page(request, slug):
    """Grand Finale Journey Step: Make a wish, blow out candles, and submit birthday wishes."""
    profile, response = _get_live_profile_or_render(request, slug)
    # If helper decided to redirect to password gate, allow wishes page to still render
    # (sharing flow may show a public view). Fall back to loading profile directly.
    if response:
        try:
            from apps.profiles.models import BirthdayProfile
            profile = BirthdayProfile.objects.filter(slug=slug).select_related('theme').first()
            if not profile:
                return response
        except Exception:
            return response

    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    # Determine whether this view should allow submissions.
    # If `?public=1` is present, render in recipient/public view-only mode (no submission form)
    # and hide the global header so recipients don't see creator navigation.
    allow_submit = request.GET.get('public') != '1'
    hide_header = request.GET.get('public') == '1'

    # Handle AJAX Wish Submission
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = WishSubmissionForm(request.POST)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.birthday_profile = profile
            wish.candle_blown = request.POST.get("candle_blown") == "true"
            wish.save()
            return JsonResponse({
                "success": True,
                "sender_name": wish.sender_name,
                "message": wish.message,
                "created_at": wish.created_at.strftime("%b %d, %Y %I:%M %p")
            })
        return JsonResponse({"success": False, "errors": form.errors})

    approved_wishes = profile.wishes.filter(is_approved=True)
    form = WishSubmissionForm()

    context = {
        "profile": profile,
        "wishes": approved_wishes,
        "form": form,
        "allow_submit": allow_submit,
        "hide_header": hide_header,
        "theme": theme,
        "current_step": 9,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/secret/",
        "next_url": f"/{profile.slug}/card/",
    }
    return render(request, "wishes/index.html", context)
