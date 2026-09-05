from django import forms
from .models import WishSubmission


class WishSubmissionForm(forms.ModelForm):
    class Meta:
        model = WishSubmission
        fields = ["sender_name", "message"]
        widgets = {
            "sender_name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "Your Name (e.g. Rahul, Priya & Family)"
            }),
            "message": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full px-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition",
                "placeholder": "Write your warm birthday message or blessing..."
            }),
        }
