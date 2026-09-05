from django import forms
from .models import BackgroundMusic


class BackgroundMusicForm(forms.ModelForm):
    class Meta:
        model = BackgroundMusic
        fields = ["title", "artist", "audio_file", "external_url", "is_primary", "display_order"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. Perfect (Acoustic)"
            }),
            "artist": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. Ed Sheeran"
            }),
            "audio_file": forms.FileInput(attrs={
                "class": "w-full text-slate-300 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-rose-500/20 file:text-rose-300 hover:file:bg-rose-500/30 cursor-pointer"
            }),
            "external_url": forms.URLInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "https://example.com/audio.mp3"
            }),
            "is_primary": forms.CheckboxInput(attrs={
                "class": "w-5 h-5 rounded bg-slate-900 border-slate-700 text-rose-500 focus:ring-rose-500 focus:ring-offset-slate-900 cursor-pointer"
            }),
            "display_order": forms.NumberInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white focus:outline-none focus:border-rose-500 transition",
                "min": "0"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["audio_file"].required = False
