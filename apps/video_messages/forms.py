from django import forms
from .models import VideoMessage


class VideoMessageForm(forms.ModelForm):
    class Meta:
        model = VideoMessage
        fields = ["sender_name", "relationship", "video_file", "video_url", "thumbnail", "message_text", "display_order"]
        widgets = {
            "sender_name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. Mom & Dad, Rahul & Friends"
            }),
            "relationship": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. Parents, Best Friend, Sister"
            }),
            "video_file": forms.FileInput(attrs={
                "class": "w-full text-slate-300 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-rose-500/20 file:text-rose-300 hover:file:bg-rose-500/30 cursor-pointer"
            }),
            "video_url": forms.URLInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "https://www.youtube.com/watch?v=... or Vimeo link"
            }),
            "thumbnail": forms.FileInput(attrs={
                "class": "w-full text-slate-300 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-rose-500/20 file:text-rose-300 hover:file:bg-rose-500/30 cursor-pointer"
            }),
            "message_text": forms.Textarea(attrs={
                "rows": 3,
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "Optional written wish or note..."
            }),
            "display_order": forms.NumberInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white focus:outline-none focus:border-rose-500 transition",
                "min": "0"
            }),
        }
