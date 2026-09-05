from django import forms
from .models import LoveNote


class LoveNoteForm(forms.ModelForm):
    class Meta:
        model = LoveNote
        fields = ["title", "message", "icon", "display_order"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. Your Kind Heart"
            }),
            "message": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "Write your heartfelt love note here..."
            }),
            "icon": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. ❤️, 💖, 🌟, 🌺, ✨"
            }),
            "display_order": forms.NumberInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white focus:outline-none focus:border-rose-500 transition",
                "min": "0"
            }),
        }
