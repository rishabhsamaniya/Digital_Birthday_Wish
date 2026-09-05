from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
import ast
import json
from apps.themes.models import Theme
from apps.music.models import BackgroundMusic
from apps.secret_message.models import SecretMessage
from .models import BirthdayProfile, RESERVED_SLUGS
from .forms import BirthdayProfileCreateForm
from .formsets import (
    MemoryFormSet,
    TimelineFormSet,
    LoveNoteFormSet,
    GalleryFormSet,
    VideoMessageFormSet,
)
from .services.qr_service import generate_qr_code_image
from .services.ai_wishes_service import get_ai_message_suggestions


# ─── Creator Wizard ──────────────────────────────────────────────────────────

@login_required
def create_wizard(request):
    """Multi-step interactive profile creator wizard for users."""
    if request.method == "POST":
        form = BirthdayProfileCreateForm(request.POST, request.FILES)
        memory_formset = MemoryFormSet(request.POST, request.FILES, prefix="memories")
        timeline_formset = TimelineFormSet(request.POST, request.FILES, prefix="timeline")
        love_note_formset = LoveNoteFormSet(request.POST, request.FILES, prefix="love_notes")
        gallery_formset = GalleryFormSet(request.POST, request.FILES, prefix="gallery")
        video_formset = VideoMessageFormSet(request.POST, request.FILES, prefix="videos")

        all_valid = (
            form.is_valid()
            and memory_formset.is_valid()
            and timeline_formset.is_valid()
            and love_note_formset.is_valid()
            and gallery_formset.is_valid()
            and video_formset.is_valid()
        )

        if all_valid:
            # Save main profile
            profile = form.save(commit=False)
            profile.created_by = request.user
            profile.save()

            # Save all section formsets
            memory_formset.instance = profile
            memory_formset.save()

            timeline_formset.instance = profile
            timeline_formset.save()

            love_note_formset.instance = profile
            love_note_formset.save()

            gallery_formset.instance = profile
            gallery_formset.save()

            video_formset.instance = profile
            video_formset.save()

            # Handle optional background music
            music_title = request.POST.get("music_title", "").strip()
            music_url = request.POST.get("music_url", "").strip()
            music_file = request.FILES.get("music_file")
            if music_title or music_url or music_file:
                BackgroundMusic.objects.create(
                    birthday_profile=profile,
                    title=music_title or "Background Music Track",
                    external_url=music_url or "",
                    audio_file=music_file,
                    is_primary=True,
                )

            # Handle optional Secret Message
            secret_text = request.POST.get("secret_text", "").strip()
            pin_code = request.POST.get("pin_code", "").strip()
            hint = request.POST.get("hint", "").strip()
            if secret_text:
                SecretMessage.objects.create(
                    birthday_profile=profile,
                    title="Surprise Secret Message 🔒",
                    secret_text=secret_text,
                    pin_code=pin_code if pin_code else None,
                    hint=hint or "",
                )

            # Auto-unlock for the creator in their own session
            request.session[f"profile_unlocked_{profile.slug}"] = True

            messages.success(
                request,
                f"🎉 Birthday Wish Page for {profile.full_name} created successfully!"
            )
            return redirect("profiles:creation_success", slug=profile.slug)

        else:
            # Log detailed errors to help debugging when users see the generic message
            logger = logging.getLogger(__name__)
            try:
                logger.warning("Create wizard validation failed: form errors=%s", form.errors.as_json())
            except Exception:
                logger.warning("Create wizard validation failed: form errors=%s", form.errors)

            # Log each formset's errors
            for name, fs in (
                ("memory_formset", memory_formset),
                ("timeline_formset", timeline_formset),
                ("love_note_formset", love_note_formset),
                ("gallery_formset", gallery_formset),
                ("video_formset", video_formset),
            ):
                try:
                    logger.warning("%s errors: %s", name, fs.errors)
                except Exception:
                    logger.warning("%s had errors (unserializable)", name)

            messages.error(request, "Please fix the errors below and try again.")
    else:
        form = BirthdayProfileCreateForm()
        memory_formset = MemoryFormSet(prefix="memories")
        timeline_formset = TimelineFormSet(prefix="timeline")
        love_note_formset = LoveNoteFormSet(prefix="love_notes")
        gallery_formset = GalleryFormSet(prefix="gallery")
        video_formset = VideoMessageFormSet(prefix="videos")

    ai_suggestions = get_ai_message_suggestions()
    # Pre-serialize to JSON for safe embedding in templates/JS
    import json
    ai_suggestions_json = json.dumps(ai_suggestions)
    # Find primary background music (if any) for this profile (only available after save)
    try:
        primary_track = BackgroundMusic.objects.filter(birthday_profile=profile, is_primary=True).first() or profile.music_tracks.first()
    except Exception:
        primary_track = None
    themes = Theme.objects.all()

    context = {
        "form": form,
        "memory_formset": memory_formset,
        "timeline_formset": timeline_formset,
        "love_note_formset": love_note_formset,
        "gallery_formset": gallery_formset,
        "video_formset": video_formset,
        "ai_suggestions": ai_suggestions,
        "ai_suggestions_json": ai_suggestions_json,
        "primary_track": primary_track,
        "themes": themes,
    }
    return render(request, "profiles/create_wizard.html", context)


@login_required
def creation_success(request, slug):
    """Success page shown after profile creation — displays URL, password, and QR code."""
    profile = get_object_or_404(BirthdayProfile, slug=slug, created_by=request.user)
    profile_url = request.build_absolute_uri(f"/{profile.slug}/")
    public_wish_url = request.build_absolute_uri(f"/{profile.slug}/wish/?public=1")
    context = {
        "profile": profile,
        "profile_url": profile_url,
        "plain_password": profile.plain_password_hint,
        "public_wish_url": public_wish_url,
    }
    return render(request, "profiles/creation_success.html", context)


@login_required
def my_profiles(request):
    """Dashboard view listing profiles created by the current user."""
    user_profiles = BirthdayProfile.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "profiles/my_profiles.html", {"profiles": user_profiles})


# ─── Password Gate ──────────────────────────────────────────────────────────

def profile_password_gate(request, slug):
    """Password lock screen for protected birthday profiles."""
    slug = slug.lower().strip()
    profile = BirthdayProfile.objects.filter(slug=slug).first()
    if not profile:
        raise Http404("Birthday profile not found.")

    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    if request.method == "POST":
        entered = request.POST.get("access_password", "").strip()
        if profile.check_access_password(entered):
            request.session[f"profile_unlocked_{slug}"] = True
            return redirect(f"/{slug}/")
        else:
            return render(request, "profiles/password_gate.html", {
                "profile": profile,
                "theme": theme,
                "error": "Incorrect password. Please try again! 🔒",
            })

    return render(request, "profiles/password_gate.html", {
        "profile": profile,
        "theme": theme,
    })


# ─── Profile Journey Helper ──────────────────────────────────────────────────

def _get_live_profile_or_render(request, slug):
    """
    Helper to fetch profile by slug and validate active status, schedule, and expiry.
    Also checks password-protection session gate.
    """
    slug = slug.lower().strip()

    if slug in RESERVED_SLUGS:
        raise Http404("Invalid profile URL path.")

    profile = BirthdayProfile.objects.filter(slug=slug).select_related("theme").first()
    if not profile:
        raise Http404("Birthday profile not found.")

    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    # Check active status
    if not profile.is_active:
        return None, render(request, "profiles/inactive.html", {"profile": profile, "theme": theme}, status=403)

    now = timezone.now()

    # Check scheduled publishing date
    if profile.publish_date and now < profile.publish_date:
        return None, render(request, "profiles/scheduled.html", {"profile": profile, "theme": theme}, status=200)

    # Check expiration date and behavior
    if profile.expiry_date and now > profile.expiry_date:
        if profile.expiry_behavior == BirthdayProfile.EXPIRY_MAKE_PRIVATE:
            return None, render(request, "profiles/expired.html", {"profile": profile, "theme": theme}, status=403)

    # ── Password Gate check ──────────────────────────────────────────
    if profile.is_password_protected:
        session_key = f"profile_unlocked_{slug}"
        is_creator = request.user.is_authenticated and profile.created_by == request.user
        is_staff = request.user.is_authenticated and request.user.is_staff
        already_unlocked = request.session.get(session_key, False)

        if not (already_unlocked or is_creator or is_staff):
            from django.shortcuts import redirect as _redirect
            return None, _redirect(f"/{slug}/unlock/")

    return profile, None


# ─── Journey Steps ──────────────────────────────────────────────────────────

def _get_display_message(profile):
    """Return a clean profile message, including recovery of older AI selections."""
    display_message = (profile.final_message or "").strip()
    if display_message.startswith("{"):
        try:
            saved_message = json.loads(display_message)
        except (json.JSONDecodeError, TypeError):
            try:
                saved_message = ast.literal_eval(display_message)
            except (ValueError, SyntaxError):
                saved_message = {}
        if isinstance(saved_message, dict):
            display_message = str(saved_message.get("message", "")).strip()

    if not display_message:
        display_message = get_ai_message_suggestions()[0]["message"]
    return display_message

def profile_detail(request, slug):
    """Step 1: Dynamic profile landing view."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    context = {
        "profile": profile,
        "theme": theme,
        "current_step": 1,
        "total_steps": 9,
        "prev_url": None,
        "next_url": f"/{profile.slug}/birthday/",
    }
    return render(request, "profiles/landing.html", context)


def birthday_reveal(request, slug):
    """Step 2: Cinematic Birthday Reveal view."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    display_message = _get_display_message(profile)

    context = {
        "profile": profile,
        "theme": theme,
        "display_message": display_message,
        "current_step": 2,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/",
        "next_url": f"/{profile.slug}/countdown/",
    }
    return render(request, "profiles/birthday_reveal.html", context)


def countdown_timer(request, slug):
    """Step 3: Live Countdown timer view."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    theme = profile.theme or Theme.objects.filter(is_default=True).first()

    context = {
        "profile": profile,
        "theme": theme,
        "current_step": 3,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/birthday/",
        "next_url": f"/{profile.slug}/memories/",
    }
    return render(request, "profiles/countdown.html", context)


def birthday_card(request, slug):
    """Grand Finale: Digital Birthday Greeting Card view."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    theme = profile.theme or Theme.objects.filter(is_default=True).first()
    wishes_count = profile.wishes.filter(is_approved=True).count()
    memories_count = profile.memories.count()
    love_notes_count = profile.love_notes.count()

    context = {
        "profile": profile,
        "theme": theme,
        "display_message": _get_display_message(profile),
        "wishes_count": wishes_count,
        "memories_count": memories_count,
        "love_notes_count": love_notes_count,
        "current_step": 9,
        "total_steps": 9,
        "prev_url": f"/{profile.slug}/wish/",
        "next_url": f"/{profile.slug}/",
    }
    return render(request, "profiles/card.html", context)


def profile_qr_code(request, slug):
    """Public QR Code image endpoint returning PNG stream."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    profile_url = request.build_absolute_uri(f"/{profile.slug}/")
    qr_buffer = generate_qr_code_image(profile_url)

    res = HttpResponse(qr_buffer.getvalue(), content_type="image/png")
    res["Content-Disposition"] = f'inline; filename="{profile.slug}-qr.png"'
    return res


def profile_qr_code_wish(request, slug):
    """Public QR Code image endpoint returning PNG stream for the wishes page URL."""
    profile, response = _get_live_profile_or_render(request, slug)
    if response:
        return response

    wish_url = request.build_absolute_uri(f"/{profile.slug}/wish/?public=1")
    qr_buffer = generate_qr_code_image(wish_url)

    res = HttpResponse(qr_buffer.getvalue(), content_type="image/png")
    res["Content-Disposition"] = f'inline; filename="{profile.slug}-wish-qr.png"'
    return res


def custom_404_view(request, exception=None):
    """Custom 404 handler returning styled error page."""
    return render(request, "404.html", status=404)
