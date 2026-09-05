from django import forms
from .models import SecretMessage


class SecretMessageForm(forms.ModelForm):
    class Meta:
        model = SecretMessage
        fields = ["title", "secret_text", "pin_code", "hint", "image"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. For Your Eyes Only 🔒"
            }),
            "secret_text": forms.Textarea(attrs={
                "rows": 5,
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "Write your confidential secret message here..."
            }),
            "pin_code": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. 1234, 0415 (Leave empty for no lock)"
            }),
            "hint": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "e.g. Our anniversary date (DDMM)"
            }),
            "image": forms.FileInput(attrs={
                "class": "w-full text-slate-300 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-rose-500/20 file:text-rose-300 hover:file:bg-rose-500/30 cursor-pointer"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["image"].required = False
