from django.shortcuts import render


def home(request):
    return render(request, "base.html", {"page": "pages/home.html"})


def login(request):
    return render(request, "base.html", {"page": "pages/login.html"})


def signup(request):
    return render(request, "base.html", {"page": "pages/signup.html"})

