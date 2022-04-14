from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "base.html", {"page": "pages/home.html"})


def login(request):
    return render(request, "base.html", {"page": "pages/login.html", "form": LoginForm()})


def signup(request):
    return render(request, "base.html", {"page": "pages/signup.html", "form": SignupForm()})


@login_required
def profile(request):
    return render(request, "base.html", {"page": "pages/profile.html"})


def page_not_found(request, exception):
    return render(request, "base.html", {"page": "pages/404.html"})
