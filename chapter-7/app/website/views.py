from django.shortcuts import render
from .forms import SearchForm, CommentForm
from .models import Post
from .actions import POST_PER_PAGE


def all_posts(request):
    return render(
        request,
        "base.html",
        {
            "posts": Post.objects.all()[:5],
            "page": "pages/all_posts.html",
            "active_nav": "all_posts",
            "form": SearchForm(),
            "next_page": 2,
            "is_last_page": (Post.objects.count() // POST_PER_PAGE) == 2,
        },
    )


def single(request, slug):
    return render(
        request,
        "base.html",
        {
            "post": Post.objects.get(slug=slug),
            "page": "pages/single.html",
            "form": CommentForm(),
        },
    )


def about(request):
    return render(
        request,
        "base.html",
        {"page": "pages/about_us.html", "active_nav": "about"},
    )


def page_not_found(request, exception):
    return render(request, "base.html", {"page": "pages/404.html"})
