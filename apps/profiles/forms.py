from django import forms
from .models import BirthdayProfile
from apps.themes.models import Theme


class BirthdayProfileCreateForm(forms.ModelForm):
    class Meta:
        model = BirthdayProfile
        fields = [
            "full_name",
            "nickname",
            "slug",
            "birthday_date",
            "theme",
            "profile_image",
            "cover_image",
            "intro_message",
            "final_message",
            "special_letter",
            "enable_animations",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-black/40 border border-white/15 text-white placeholder-gray-500 focus:outline-none focus:border-rose-400 transition-all text-sm",
                "placeholder": "e.g., Sneha Sharma"
            }),
            "nickname": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-black/40 border border-white/15 text-white placeholder-gray-500 focus:outline-none focus:border-rose-400 transition-all text-sm",
                "placeholder": "e.g., Snehu or Pree"
            }),
            "slug": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-black/40 border border-white/15 text-white placeholder-gray-500 focus:outline-none focus:border-rose-400 transition-all text-sm",
                "placeholder": "e.g., sneha (URL will be /sneha/)"
            }),
            "birthday_date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full px-4 py-3 rounded-xl bg-black/40 border border-white/15 text-white placeholder-gray-500 focus:outline-none focus:border-rose-400 transition-all text-sm"
            }),
            "theme": forms.Select(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-black/40 border border-white/15 text-white focus:outline-none focus:border-rose-400 transition-all text-sm"
            }),
            "profile_image": forms.FileInput(attrs={
                "class": "w-full text-sm text-gray-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-rose-500/20 file:text-rose-300 hover:file:bg-rose-500/30 cursor-pointer"
            }),
            "cover_image": forms.FileInput(attrs={
                "class": "w-full text-sm text-gray-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-rose-500/20 file:text-rose-300 hover:file:bg-rose-500/30 cursor-pointer"
            }),
            "intro_message": forms.Textarea(attrs={
                "id": "id_intro_message",
                "rows": 3,
                "class": "w-full px-4 py-3 rounded-xl bg-black/40 border border-white/15 text-white placeholder-gray-500 focus:outline-none focus:border-rose-400 transition-all text-sm",
                "placeholder": "Welcome greeting for the landing page..."
            }),
            "final_message": forms.Textarea(attrs={
                "id": "id_final_message",
                "rows": 3,
                "class": "w-full px-4 py-3 rounded-xl bg-black/40 border border-white/15 text-white placeholder-gray-500 focus:outline-none focus:border-rose-400 transition-all text-sm",
                "placeholder": "Heartfelt closing birthday message..."
            }),
            "special_letter": forms.Textarea(attrs={
                "id": "id_special_letter",
                "rows": 4,
                "class": "w-full px-4 py-3 rounded-xl bg-black/40 border border-white/15 text-white placeholder-gray-500 focus:outline-none focus:border-rose-400 transition-all text-sm",
                "placeholder": "Personal letter or special note..."
            }),
        }


BirthdayProfileForm = BirthdayProfileCreateForm

