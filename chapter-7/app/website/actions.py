from .models import Post, Comment
from .forms import SearchForm, CommentForm
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from django.urls import reverse

POST_PER_PAGE = 5


def send_page(self, data={}):
    """Render HTML and send page to client"""

    # Prepare context data for page
    page = data["page"]
    context = {}
    data_reverse = {}
    match page:
        case "all posts":
            context = {
                "posts": Post.objects.all()[:POST_PER_PAGE],
                "form": SearchForm(),
                "next_page": 2,
                "is_last_page": (Post.objects.count() // POST_PER_PAGE) == 2,
            }
        case "single post":
            post = Post.objects.get(id=data["id"])
            context = {
                "post": post,
                "form": CommentForm(),
                "comments": Comment.objects.filter(post=post),
            }
            data_reverse = {"slug": post.slug}

    # Render HTML nav and send to client
    context.update({"active_nav": page})
    self.send_html(
        {
            "selector": "#nav",
            "html": render_to_string("components/_nav.html", context),
        }
    )

    # Render HTML page and send to client
    template_page = page.replace(" ", "_")
    self.send_html(
        {
            "selector": "#main",
            "html": render_to_string(f"pages/{template_page}.html", context),
            "url": reverse(page, kwargs=data_reverse),
        }
    )


def search(self, data={}):
    """Search for posts"""
    # Prepare context data for page
    context = {
        "posts": Post.objects.filter(title__icontains=data["search"])[:POST_PER_PAGE]
    }

    # Render HTML page and send to client
    self.send_html(
        {
            "selector": "#all-posts",
            "html": render_to_string("components/all_posts/list.html", context),
        }
    )


def add_next_posts(self, data={}):
    """Add next posts from pagination"""
    # Prepare context data for page
    page = int(data["page"]) if "page" in data else 1
    start_of_slice = (page - 1) * POST_PER_PAGE
    end_of_slice = start_of_slice + POST_PER_PAGE
    context = {
        "posts": Post.objects.all()[start_of_slice:end_of_slice],
        "next_page": page + 1,
        "is_last_page": (Post.objects.count() // POST_PER_PAGE) == page,
    }

    # Add and render HTML with new posts
    self.send_html(
        {
            "selector": "#all-posts",
            "html": render_to_string("components/all_posts/list.html", context),
            "append": True,
        }
    )

    # Update paginator
    self.send_html(
        {
            "selector": "#paginator",
            "html": render_to_string(
                "components/all_posts/_button_paginator.html", context
            ),
        }
    )


def add_comment(self, data):
    """Add new comment to database"""
    # Add post
    data_with_post = data.copy()
    post = Post.objects.get(id=data["post_id"])
    data_with_post["post"] = post
    # Set initial values by CommentForm
    form = CommentForm(data_with_post)
    # Check if form is valid
    if form.is_valid():
        # Save comment
        form.save()
        # Render HTML with new comment to all clients
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type": "send.html",  # Run "send_html()" method
                "selector": "#comments",
                "html": render_to_string(
                    "components/_single_comment.html", {"comment": data}
                ),
                "append": True,
                "broadcast": True,
                "url": reverse("single post", kwargs={"slug": post.slug}),
            },
        )
