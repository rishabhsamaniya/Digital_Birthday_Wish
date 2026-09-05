from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.profiles.models import BirthdayProfile
from apps.profiles.forms import BirthdayProfileForm
from apps.profiles.services.qr_service import generate_qr_code_image
from apps.memories.models import Memory
from apps.memories.forms import MemoryForm
from apps.timeline.models import TimelineEvent
from apps.timeline.forms import TimelineEventForm
from apps.love_notes.models import LoveNote
from apps.love_notes.forms import LoveNoteForm
from apps.gallery.models import GalleryPhoto
from apps.gallery.forms import GalleryPhotoForm
from apps.music.models import BackgroundMusic
from apps.music.forms import BackgroundMusicForm
from apps.video_messages.models import VideoMessage
from apps.video_messages.forms import VideoMessageForm
from apps.secret_message.models import SecretMessage
from apps.secret_message.forms import SecretMessageForm
from apps.wishes.models import WishSubmission


def dashboard_login(request):
    """Admin login view for dashboard access."""
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard:index")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "dashboard/login.html", {"form": form})


def dashboard_logout(request):
    """Log out admin user and redirect to login page."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("dashboard:login")


@login_required(login_url="dashboard:login")
def dashboard_index(request):
    """Dashboard overview screen with aggregate metrics and recent profiles."""
    total_profiles = BirthdayProfile.objects.count()
    active_profiles = BirthdayProfile.objects.filter(is_active=True).count()
    total_memories = Memory.objects.count()
    total_photos = GalleryPhoto.objects.count()
    total_music = BackgroundMusic.objects.count()
    total_videos = VideoMessage.objects.count()
    total_wishes = WishSubmission.objects.count()

    recent_profiles = BirthdayProfile.objects.select_related("theme").order_by("-created_at")[:6]

    context = {
        "total_profiles": total_profiles,
        "active_profiles": active_profiles,
        "total_memories": total_memories,
        "total_photos": total_photos,
        "total_music": total_music,
        "total_videos": total_videos,
        "total_wishes": total_wishes,
        "recent_profiles": recent_profiles,
    }
    return render(request, "dashboard/index.html", context)


@login_required(login_url="dashboard:login")
def profile_list(request):
    """List all birthday profiles with quick status controls."""
    query = request.GET.get("q", "")
    profiles = BirthdayProfile.objects.select_related("theme").order_by("-created_at")

    if query:
        profiles = profiles.filter(full_name__icontains=query) | profiles.filter(slug__icontains=query)

    context = {
        "profiles": profiles,
        "query": query,
    }
    return render(request, "dashboard/profile_list.html", context)


@login_required(login_url="dashboard:login")
def profile_create(request):
    """Create a new birthday profile."""
    if request.method == "POST":
        form = BirthdayProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()
            messages.success(request, f"Birthday profile for '{profile.full_name}' created successfully!")
            return redirect("dashboard:profile_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BirthdayProfileForm()

    return render(request, "dashboard/profile_form.html", {
        "form": form,
        "title": "Create New Birthday Profile",
        "action": "Create Profile"
    })


@login_required(login_url="dashboard:login")
def profile_edit(request, pk):
    """Edit an existing birthday profile."""
    profile = get_object_or_404(BirthdayProfile, pk=pk)

    if request.method == "POST":
        form = BirthdayProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.success(request, f"Profile for '{profile.full_name}' updated successfully!")
            return redirect("dashboard:profile_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BirthdayProfileForm(instance=profile)

    return render(request, "dashboard/profile_form.html", {
        "form": form,
        "profile": profile,
        "title": f"Edit Profile: {profile.full_name}",
        "action": "Update Profile"
    })


@login_required(login_url="dashboard:login")
def profile_delete(request, pk):
    """Delete a birthday profile with confirmation."""
    profile = get_object_or_404(BirthdayProfile, pk=pk)

    if request.method == "POST":
        name = profile.full_name
        profile.delete()
        messages.success(request, f"Profile '{name}' deleted successfully.")
        return redirect("dashboard:profile_list")

    return render(request, "dashboard/profile_confirm_delete.html", {"profile": profile})


@login_required(login_url="dashboard:login")
def profile_toggle_status(request, pk):
    """Quick action to toggle active status on a profile."""
    profile = get_object_or_404(BirthdayProfile, pk=pk)
    profile.is_active = not profile.is_active
    profile.save(update_fields=["is_active", "updated_at"])

    status_str = "activated" if profile.is_active else "deactivated"
    messages.success(request, f"Profile '{profile.full_name}' is now {status_str}.")
    return redirect("dashboard:profile_list")


@login_required(login_url="dashboard:login")
def profile_qr(request, pk):
    """Dashboard view to preview/download QR Code for a Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=pk)
    profile_url = request.build_absolute_uri(f"/{profile.slug}/")
    qr_buffer = generate_qr_code_image(profile_url)

    res = HttpResponse(qr_buffer.getvalue(), content_type="image/png")
    res["Content-Disposition"] = f'attachment; filename="{profile.slug}-birthday-qr.png"'
    return res


# MEMORIES DASHBOARD MANAGEMENT VIEWS

@login_required(login_url="dashboard:login")
def memory_list(request, profile_id):
    """List all memories belonging to a specific Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)
    memories = profile.memories.all()
    return render(request, "dashboard/memory_list.html", {
        "profile": profile,
        "memories": memories,
    })


@login_required(login_url="dashboard:login")
def memory_create(request, profile_id):
    """Add a new memory to a specific Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)

    if request.method == "POST":
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.birthday_profile = profile
            memory.save()
            messages.success(request, f"Memory '{memory.title}' added successfully to {profile.full_name}!")
            return redirect("dashboard:memory_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = MemoryForm()

    return render(request, "dashboard/memory_form.html", {
        "form": form,
        "profile": profile,
        "title": f"Add Memory for {profile.full_name}",
        "action": "Save Memory"
    })


@login_required(login_url="dashboard:login")
def memory_edit(request, pk):
    """Edit an existing memory."""
    memory = get_object_or_404(Memory, pk=pk)
    profile = memory.birthday_profile

    if request.method == "POST":
        form = MemoryForm(request.POST, request.FILES, instance=memory)
        if form.is_valid():
            form.save()
            messages.success(request, f"Memory '{memory.title}' updated successfully!")
            return redirect("dashboard:memory_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = MemoryForm(instance=memory)

    return render(request, "dashboard/memory_form.html", {
        "form": form,
        "memory": memory,
        "profile": profile,
        "title": f"Edit Memory: {memory.title}",
        "action": "Update Memory"
    })


@login_required(login_url="dashboard:login")
def memory_delete(request, pk):
    """Delete a memory with confirmation."""
    memory = get_object_or_404(Memory, pk=pk)
    profile_id = memory.birthday_profile.pk

    if request.method == "POST":
        title = memory.title
        memory.delete()
        messages.success(request, f"Memory '{title}' deleted successfully.")
        return redirect("dashboard:memory_list", profile_id=profile_id)

    return render(request, "dashboard/memory_confirm_delete.html", {"memory": memory})


# TIMELINE DASHBOARD MANAGEMENT VIEWS

@login_required(login_url="dashboard:login")
def timeline_list(request, profile_id):
    """List all timeline events for a specific Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)
    events = profile.timeline_events.all()
    return render(request, "dashboard/timeline_list.html", {
        "profile": profile,
        "events": events,
    })


@login_required(login_url="dashboard:login")
def timeline_create(request, profile_id):
    """Add a new timeline event for a profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)

    if request.method == "POST":
        form = TimelineEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.birthday_profile = profile
            event.save()
            messages.success(request, f"Timeline milestone '{event.title}' added successfully!")
            return redirect("dashboard:timeline_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = TimelineEventForm()

    return render(request, "dashboard/timeline_form.html", {
        "form": form,
        "profile": profile,
        "title": f"Add Timeline Event for {profile.full_name}",
        "action": "Save Event"
    })


@login_required(login_url="dashboard:login")
def timeline_edit(request, pk):
    """Edit an existing timeline event."""
    event = get_object_or_404(TimelineEvent, pk=pk)
    profile = event.birthday_profile

    if request.method == "POST":
        form = TimelineEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f"Timeline milestone '{event.title}' updated successfully!")
            return redirect("dashboard:timeline_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = TimelineEventForm(instance=event)

    return render(request, "dashboard/timeline_form.html", {
        "form": form,
        "event": event,
        "profile": profile,
        "title": f"Edit Timeline Event: {event.title}",
        "action": "Update Event"
    })


@login_required(login_url="dashboard:login")
def timeline_delete(request, pk):
    """Delete a timeline event with confirmation."""
    event = get_object_or_404(TimelineEvent, pk=pk)
    profile_id = event.birthday_profile.pk

    if request.method == "POST":
        title = event.title
        event.delete()
        messages.success(request, f"Timeline event '{title}' deleted successfully.")
        return redirect("dashboard:timeline_list", profile_id=profile_id)

    return render(request, "dashboard/timeline_confirm_delete.html", {"event": event})


# LOVE NOTES DASHBOARD MANAGEMENT VIEWS

@login_required(login_url="dashboard:login")
def love_note_list(request, profile_id):
    """List all love notes for a specific Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)
    notes = profile.love_notes.all()
    return render(request, "dashboard/love_note_list.html", {
        "profile": profile,
        "notes": notes,
    })


@login_required(login_url="dashboard:login")
def love_note_create(request, profile_id):
    """Add a new love note for a profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)

    if request.method == "POST":
        form = LoveNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.birthday_profile = profile
            note.save()
            messages.success(request, f"Love note '{note.title}' added successfully!")
            return redirect("dashboard:love_note_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = LoveNoteForm()

    return render(request, "dashboard/love_note_form.html", {
        "form": form,
        "profile": profile,
        "title": f"Add Love Note for {profile.full_name}",
        "action": "Save Note"
    })


@login_required(login_url="dashboard:login")
def love_note_edit(request, pk):
    """Edit an existing love note."""
    note = get_object_or_404(LoveNote, pk=pk)
    profile = note.birthday_profile

    if request.method == "POST":
        form = LoveNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, f"Love note '{note.title}' updated successfully!")
            return redirect("dashboard:love_note_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = LoveNoteForm(instance=note)

    return render(request, "dashboard/love_note_form.html", {
        "form": form,
        "note": note,
        "profile": profile,
        "title": f"Edit Love Note: {note.title}",
        "action": "Update Note"
    })


@login_required(login_url="dashboard:login")
def love_note_delete(request, pk):
    """Delete a love note with confirmation."""
    note = get_object_or_404(LoveNote, pk=pk)
    profile_id = note.birthday_profile.pk

    if request.method == "POST":
        title = note.title
        note.delete()
        messages.success(request, f"Love note '{title}' deleted successfully.")
        return redirect("dashboard:love_note_list", profile_id=profile_id)

    return render(request, "dashboard/love_note_confirm_delete.html", {"note": note})


# GALLERY DASHBOARD MANAGEMENT VIEWS

@login_required(login_url="dashboard:login")
def gallery_list(request, profile_id):
    """List all gallery photos for a specific Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)
    photos = profile.photos.all()
    return render(request, "dashboard/gallery_list.html", {
        "profile": profile,
        "photos": photos,
    })


@login_required(login_url="dashboard:login")
def gallery_create(request, profile_id):
    """Add a new photo to a specific Birthday Profile gallery."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)

    if request.method == "POST":
        form = GalleryPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.birthday_profile = profile
            photo.save()
            messages.success(request, f"Gallery photo added successfully!")
            return redirect("dashboard:gallery_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = GalleryPhotoForm()

    return render(request, "dashboard/gallery_form.html", {
        "form": form,
        "profile": profile,
        "title": f"Add Gallery Photo for {profile.full_name}",
        "action": "Upload Photo"
    })


@login_required(login_url="dashboard:login")
def gallery_edit(request, pk):
    """Edit an existing gallery photo details."""
    photo = get_object_or_404(GalleryPhoto, pk=pk)
    profile = photo.birthday_profile

    if request.method == "POST":
        form = GalleryPhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Gallery photo updated successfully!")
            return redirect("dashboard:gallery_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = GalleryPhotoForm(instance=photo)

    return render(request, "dashboard/gallery_form.html", {
        "form": form,
        "photo": photo,
        "profile": profile,
        "title": f"Edit Gallery Photo details",
        "action": "Update Photo"
    })


@login_required(login_url="dashboard:login")
def gallery_delete(request, pk):
    """Delete a gallery photo with confirmation."""
    photo = get_object_or_404(GalleryPhoto, pk=pk)
    profile_id = photo.birthday_profile.pk

    if request.method == "POST":
        photo.delete()
        messages.success(request, "Gallery photo deleted successfully.")
        return redirect("dashboard:gallery_list", profile_id=profile_id)

    return render(request, "dashboard/gallery_confirm_delete.html", {"photo": photo})


# MUSIC DASHBOARD MANAGEMENT VIEWS

@login_required(login_url="dashboard:login")
def music_list(request, profile_id):
    """List all music tracks for a specific Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)
    tracks = profile.music_tracks.all()
    return render(request, "dashboard/music_list.html", {
        "profile": profile,
        "tracks": tracks,
    })


@login_required(login_url="dashboard:login")
def music_create(request, profile_id):
    """Add a new music track to a Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)

    if request.method == "POST":
        form = BackgroundMusicForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.birthday_profile = profile
            if track.is_primary:
                profile.music_tracks.filter(is_primary=True).update(is_primary=False)
            track.save()
            messages.success(request, f"Music track '{track.title}' added successfully!")
            return redirect("dashboard:music_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BackgroundMusicForm()

    return render(request, "dashboard/music_form.html", {
        "form": form,
        "profile": profile,
        "title": f"Add Music Track for {profile.full_name}",
        "action": "Add Track"
    })


@login_required(login_url="dashboard:login")
def music_edit(request, pk):
    """Edit an existing music track."""
    track = get_object_or_404(BackgroundMusic, pk=pk)
    profile = track.birthday_profile

    if request.method == "POST":
        form = BackgroundMusicForm(request.POST, request.FILES, instance=track)
        if form.is_valid():
            track = form.save(commit=False)
            if track.is_primary:
                profile.music_tracks.exclude(pk=track.pk).filter(is_primary=True).update(is_primary=False)
            track.save()
            messages.success(request, f"Music track '{track.title}' updated successfully!")
            return redirect("dashboard:music_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BackgroundMusicForm(instance=track)

    return render(request, "dashboard/music_form.html", {
        "form": form,
        "track": track,
        "profile": profile,
        "title": f"Edit Track: {track.title}",
        "action": "Update Track"
    })


@login_required(login_url="dashboard:login")
def music_delete(request, pk):
    """Delete a music track with confirmation."""
    track = get_object_or_404(BackgroundMusic, pk=pk)
    profile_id = track.birthday_profile.pk

    if request.method == "POST":
        title = track.title
        track.delete()
        messages.success(request, f"Music track '{title}' deleted successfully.")
        return redirect("dashboard:music_list", profile_id=profile_id)

    return render(request, "dashboard/music_confirm_delete.html", {"track": track})


# VIDEO MESSAGES DASHBOARD MANAGEMENT VIEWS

@login_required(login_url="dashboard:login")
def video_list(request, profile_id):
    """List all video messages for a specific Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)
    videos = profile.video_messages.all()
    return render(request, "dashboard/video_list.html", {
        "profile": profile,
        "videos": videos,
    })


@login_required(login_url="dashboard:login")
def video_create(request, profile_id):
    """Add a new video message for a Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)

    if request.method == "POST":
        form = VideoMessageForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.birthday_profile = profile
            video.save()
            messages.success(request, f"Video message from '{video.sender_name}' added successfully!")
            return redirect("dashboard:video_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = VideoMessageForm()

    return render(request, "dashboard/video_form.html", {
        "form": form,
        "profile": profile,
        "title": f"Add Video Message for {profile.full_name}",
        "action": "Save Video Message"
    })


@login_required(login_url="dashboard:login")
def video_edit(request, pk):
    """Edit an existing video message."""
    video = get_object_or_404(VideoMessage, pk=pk)
    profile = video.birthday_profile

    if request.method == "POST":
        form = VideoMessageForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, f"Video message from '{video.sender_name}' updated successfully!")
            return redirect("dashboard:video_list", profile_id=profile.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = VideoMessageForm(instance=video)

    return render(request, "dashboard/video_form.html", {
        "form": form,
        "video": video,
        "profile": profile,
        "title": f"Edit Video Message from {video.sender_name}",
        "action": "Update Video Message"
    })


@login_required(login_url="dashboard:login")
def video_delete(request, pk):
    """Delete a video message with confirmation."""
    video = get_object_or_404(VideoMessage, pk=pk)
    profile_id = video.birthday_profile.pk

    if request.method == "POST":
        sender = video.sender_name
        video.delete()
        messages.success(request, f"Video message from '{sender}' deleted successfully.")
        return redirect("dashboard:video_list", profile_id=profile_id)

    return render(request, "dashboard/video_confirm_delete.html", {"video": video})


# SECRET MESSAGE DASHBOARD MANAGEMENT VIEWS

@login_required(login_url="dashboard:login")
def secret_message_detail(request, profile_id):
    """Create or edit the secret message for a Birthday Profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)
    secret = getattr(profile, "secret_message", None)

    if request.method == "POST":
        form = SecretMessageForm(request.POST, request.FILES, instance=secret)
        if form.is_valid():
            sec = form.save(commit=False)
            sec.birthday_profile = profile
            sec.save()
            messages.success(request, f"Secret message for '{profile.full_name}' saved successfully!")
            return redirect("dashboard:profile_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SecretMessageForm(instance=secret)

    return render(request, "dashboard/secret_message_form.html", {
        "form": form,
        "profile": profile,
        "secret": secret,
        "title": f"Secret Message for {profile.full_name}",
        "action": "Save Secret Message"
    })


@login_required(login_url="dashboard:login")
def secret_message_delete(request, pk):
    """Delete secret message for a profile with confirmation."""
    secret = get_object_or_404(SecretMessage, pk=pk)
    profile_id = secret.birthday_profile.pk

    if request.method == "POST":
        secret.delete()
        messages.success(request, "Secret message deleted successfully.")
        return redirect("dashboard:profile_list")

    return render(request, "dashboard/secret_message_confirm_delete.html", {"secret": secret})


# WISH SUBMISSION DASHBOARD MANAGEMENT VIEWS

@login_required(login_url="dashboard:login")
def wish_list(request, profile_id):
    """List all submitted birthday wishes for a profile."""
    profile = get_object_or_404(BirthdayProfile, pk=profile_id)
    wishes = profile.wishes.all()
    return render(request, "dashboard/wish_list.html", {
        "profile": profile,
        "wishes": wishes,
    })


@login_required(login_url="dashboard:login")
def wish_toggle_approval(request, pk):
    """Toggle public approval status of a wish submission."""
    wish = get_object_or_404(WishSubmission, pk=pk)
    wish.is_approved = not wish.is_approved
    wish.save(update_fields=["is_approved", "updated_at"])

    status_str = "approved" if wish.is_approved else "hidden"
    messages.success(request, f"Wish from '{wish.sender_name}' is now {status_str}.")
    return redirect("dashboard:wish_list", profile_id=wish.birthday_profile.pk)


@login_required(login_url="dashboard:login")
def wish_delete(request, pk):
    """Delete a wish submission with confirmation."""
    wish = get_object_or_404(WishSubmission, pk=pk)
    profile_id = wish.birthday_profile.pk

    if request.method == "POST":
        sender = wish.sender_name
        wish.delete()
        messages.success(request, f"Wish submission from '{sender}' deleted successfully.")
        return redirect("dashboard:wish_list", profile_id=profile_id)

    return render(request, "dashboard/wish_confirm_delete.html", {"wish": wish})
