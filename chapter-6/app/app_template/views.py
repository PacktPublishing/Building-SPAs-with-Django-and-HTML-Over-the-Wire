from django.shortcuts import render
from .forms import LoginForm, SignupForm


def home(request):
    return render(request, "base.html", {"page": "pages/home.html"})


def login(request):
    return render(request, "base.html", {"page": "pages/login.html", "form": LoginForm()})


def signup(request):
    return render(request, "base.html", {"page": "pages/signup.html", "form": SignupForm()})

