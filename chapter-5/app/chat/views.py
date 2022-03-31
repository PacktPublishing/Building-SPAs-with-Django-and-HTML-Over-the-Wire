from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def login(request):
    return render(request, "index.html", {
        "users": User.objects.all()
    })


@login_required
def chat(request):
    if request.user.is_authenticated:
        return render(request, "chat.html", {
            "users": User.objects.all().exclude(id=request.user.id)
        })
    else:
        # Redirect to login page
        return redirect(reverse("login"))
