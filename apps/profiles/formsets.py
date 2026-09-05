"""
Inline formsets for the comprehensive birthday profile creator wizard.
Each formset allows the creator to add multiple items for a given section.
"""
from django import forms
from django.forms import inlineformset_factory

from apps.profiles.models import BirthdayProfile
from apps.memories.models import Memory
from apps.timeline.models import TimelineEvent
from apps.love_notes.models import LoveNote
from apps.gallery.models import GalleryPhoto
from apps.video_messages.models import VideoMessage


# ─── Shared widget helpers ─────────────────────────────────────────────────────

def _text(placeholder="", extra=""):
    return forms.TextInput(attrs={
        "class": f"w-full px-3 py-2.5 rounded-xl bg-black/40 border border-white/15 text-white placeholder-gray-500 focus:outline-none focus:border-rose-400 text-sm {extra}",
        "placeholder": placeholder,
    })


def _textarea(placeholder="", rows=3):
    return forms.Textarea(attrs={
        "class": "w-full px-3 py-2.5 rounded-xl bg-black/40 border border-white/15 text-white placeholder-gray-500 focus:outline-none focus:border-rose-400 text-sm resize-none",
        "placeholder": placeholder,
        "rows": rows,
    })


def _date():
    return forms.DateInput(attrs={
        "type": "date",
        "class": "w-full px-3 py-2.5 rounded-xl bg-black/40 border border-white/15 text-white focus:outline-none focus:border-rose-400 text-sm",
    })


def _file():
    return forms.FileInput(attrs={
        "class": "w-full text-xs text-gray-400 file:mr-3 file:py-2 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-rose-500/20 file:text-rose-300 hover:file:bg-rose-500/30 cursor-pointer",
    })


# ─── Memory Section ─────────────────────────────────────────────────────────

class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ["title", "description", "memory_date", "image"]
        widgets = {
            "title": _text("Memory title, e.g., First Date 🌹"),
            "description": _textarea("Describe this beautiful memory..."),
            "memory_date": _date(),
            "image": _file(),
        }
        labels = {
            "title": "Memory Title",
            "description": "Story / Description",
            "memory_date": "Date of Memory",
            "image": "Photo (optional)",
        }


MemoryFormSet = inlineformset_factory(
    BirthdayProfile,
    Memory,
    form=MemoryForm,
    extra=2,
    max_num=5,
    can_delete=True,
    fk_name="birthday_profile",
)


# ─── Timeline Section ────────────────────────────────────────────────────────

class TimelineEventForm(forms.ModelForm):
    class Meta:
        model = TimelineEvent
        fields = ["title", "description", "event_date", "icon", "image"]
        widgets = {
            "title": _text("Milestone title, e.g., We met at the café ☕"),
            "description": _textarea("What happened on this day..."),
            "event_date": _date(),
            "icon": _text("Emoji icon, e.g., ☕ 💍 ✈️", "w-20 text-center"),
            "image": _file(),
        }
        labels = {
            "title": "Event Title",
            "description": "Story",
            "event_date": "Date",
            "icon": "Icon Emoji",
            "image": "Photo (optional)",
        }


TimelineFormSet = inlineformset_factory(
    BirthdayProfile,
    TimelineEvent,
    form=TimelineEventForm,
    extra=2,
    max_num=5,
    can_delete=True,
    fk_name="birthday_profile",
)


# ─── Love Notes Section ──────────────────────────────────────────────────────

class LoveNoteForm(forms.ModelForm):
    class Meta:
        model = LoveNote
        fields = ["title", "message", "icon"]
        widgets = {
            "title": _text("e.g., Your Radiant Smile"),
            "message": _textarea("Write a heartfelt note about this quality...", rows=2),
            "icon": _text("Emoji, e.g., 💖", "w-20 text-center"),
        }
        labels = {
            "title": "What I Love About You",
            "message": "Personal Note",
            "icon": "Icon",
        }


LoveNoteFormSet = inlineformset_factory(
    BirthdayProfile,
    LoveNote,
    form=LoveNoteForm,
    extra=3,
    max_num=10,
    can_delete=True,
    fk_name="birthday_profile",
)


# ─── Gallery Photos Section ──────────────────────────────────────────────────

class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = ["image", "title", "caption"]
        widgets = {
            "image": _file(),
            "title": _text("Photo title (optional)"),
            "caption": _textarea("Caption or memory behind this photo (optional)", rows=2),
        }
        labels = {
            "image": "📷 Upload Photo",
            "title": "Title (optional)",
            "caption": "Caption (optional)",
        }


GalleryFormSet = inlineformset_factory(
    BirthdayProfile,
    GalleryPhoto,
    form=GalleryPhotoForm,
    extra=3,
    max_num=10,
    can_delete=True,
    fk_name="birthday_profile",
)


# ─── Video Messages Section ──────────────────────────────────────────────────

class VideoMessageForm(forms.ModelForm):
    class Meta:
        model = VideoMessage
        fields = ["sender_name", "relationship", "video_url", "video_file", "thumbnail", "message_text"]
        widgets = {
            "sender_name": _text("Sender name, e.g., Mom & Dad"),
            "relationship": _text("Relationship, e.g., Best Friend"),
            "video_url": _text("YouTube / Vimeo URL (optional)"),
            "video_file": _file(),
            "thumbnail": _file(),
            "message_text": _textarea("Short caption or intro text (optional)", rows=2),
        }
        labels = {
            "sender_name": "Sender Name",
            "relationship": "Relationship",
            "video_url": "Video URL (YouTube/Vimeo)",
            "video_file": "Upload Video File (MP4)",
            "thumbnail": "Thumbnail Image (optional)",
            "message_text": "Caption / Note",
        }


VideoMessageFormSet = inlineformset_factory(
    BirthdayProfile,
    VideoMessage,
    form=VideoMessageForm,
    extra=1,
    max_num=3,
    can_delete=True,
    fk_name="birthday_profile",
)
