from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.profiles.models import BirthdayProfile


def index(request):
    """Platform home page with direct Log In & Sign Up cards."""
    signup_form = UserCreationForm()
    login_form = AuthenticationForm()

    user_profiles = []
    if request.user.is_authenticated:
        user_profiles = BirthdayProfile.objects.filter(created_by=request.user).order_by("-created_at")[:5]

    context = {
        "signup_form": signup_form,
        "login_form": login_form,
        "user_profiles": user_profiles,
    }
    return render(request, "landing/index.html", context)
