from django.shortcuts import render
from django.contrib.auth.models import User


def index(request):
    return render(request, "index.html", {
        "users": User.objects.all().order_by("username")
    })