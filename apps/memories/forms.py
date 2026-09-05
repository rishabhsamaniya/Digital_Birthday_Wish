from django import forms
from .models import Memory


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ["title", "description", "memory_date", "image", "display_order"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. Our First Trip Together"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "Tell the story behind this memory..."
            }),
            "memory_date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white focus:outline-none focus:border-rose-500 transition"
            }),
            "image": forms.FileInput(attrs={
                "class": "w-full text-slate-300 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-rose-500/20 file:text-rose-300 hover:file:bg-rose-500/30 cursor-pointer"
            }),
            "display_order": forms.NumberInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white focus:outline-none focus:border-rose-500 transition",
                "min": "0"
            }),
        }
