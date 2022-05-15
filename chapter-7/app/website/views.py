from django.shortcuts import render
from .forms import SearchForm, CommentForm
from .models import Post, Comment
from .actions import POST_PER_PAGE


def all_posts(request):
    return render(
        request,
        "base.html",
        {
            "posts": Post.objects.all()[:5],
            "page": "pages/all_posts.html",
            "active_nav": "all posts",
            "form": SearchForm(),
            "next_page": 2,
            "is_last_page": (Post.objects.count() // POST_PER_PAGE) == 2,
        },
    )


def single_post(request, slug):
    post = list(filter(lambda post: post.slug == slug, Post.objects.all()))[0]
    return render(
        request,
        "base.html",
        {
            "post": post,
            "page": "pages/single_post.html",
            "active_nav": "single post",
            "comments": Comment.objects.filter(post=post),
            "form": CommentForm(),
        },
    )


def about(request):
    return render(
        request,
        "base.html",
        {"page": "pages/about_us.html", "active_nav": "about us"},
    )


def page_not_found(request, exception):
    return render(request, "base.html", {"page": "pages/404.html"})
