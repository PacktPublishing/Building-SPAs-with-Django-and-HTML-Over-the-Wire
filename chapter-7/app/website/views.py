from django.shortcuts import render
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


def all_posts(request):
    return render(
        request,
        "base.html",
        {
            "page": "pages/list_posts.html",
            "active_nav": "all_posts",
        },
    )


def single(request):
    return render(
        request,
        "base.html",
        {"page": "pages/single.html", "form": CommentForm()},
    )


def about(request):
    return render(
        request,
        "base.html",
        {"page": "pages/about.html", "active_nav": "about"},
    )


def page_not_found(request, exception):
    return render(request, "base.html", {"page": "pages/404.html"})
