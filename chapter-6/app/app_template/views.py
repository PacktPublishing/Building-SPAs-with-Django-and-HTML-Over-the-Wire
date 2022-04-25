from django.shortcuts import render
from .forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(
        request,
        "base.html",
        {
            "page": "pages/home.html",
            "active_nav": "home",
        },
    )


def login(request):
    return render(
        request,
        "base.html",
        {"page": "pages/login.html", "active_nav": "login", "form": LoginForm()},
    )


def signup(request):
    return render(
        request,
        "base.html",
        {"page": "pages/signup.html", "active_nav": "signup", "form": SignupForm()},
    )


@login_required
def profile(request):
    return render(
        request, "base.html", {"page": "pages/profile.html", "active_nav": "profile"}
    )


def page_not_found(request, exception):
    return render(request, "base.html", {"page": "pages/404.html"})
