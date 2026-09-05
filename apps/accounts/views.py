from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def user_signup(request):
    """Register a new user account."""
    if request.user.is_authenticated:
        return redirect("profiles:my_profiles")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Digital Birthday Wish, {user.username}! Your account has been created.")
            return redirect("profiles:create_wizard")
        else:
            messages.error(request, "Registration error. Please check the form errors below.")
    else:
        form = UserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


def user_login(request):
    """Log in an existing user."""
    if request.user.is_authenticated:
        return redirect("profiles:my_profiles")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_page = request.GET.get("next") or "profiles:my_profiles"
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    """Log out current user."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("landing:index")
