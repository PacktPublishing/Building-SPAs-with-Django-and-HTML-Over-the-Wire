from .models import Post, Comment
from .forms import CommentForm
from django.template.loader import render_to_string
from django.urls import reverse

POST_PER_PAGE = 5

def send_page(self, data={}):
    """Render HTML and send page to client"""

    # Prepare context data for page
    page = data["page"]
    context = {}
    match page:
        case "list":
            context = {"posts": Post.objects.all().order_by("-created_at")[:POST_PER_PAGE]}
        case "single":
            context = {"post": Post.objects.get(id=data["id"]) ,"form": CommentForm()}


    # Render HTML nav and send to client
    self.send_html({
        "selector": "#nav",
        "html": render_to_string("components/_nav.html", context),
    })

    # Render HTML page and send to client
    self.send_html({
        "selector": "#main",
        "html": render_to_string(f"pages/{page}.html", context),
        "url": reverse(page),
    })


def search(self, data={}):
    """Search for posts"""
    # Prepare context data for page
    context = {"posts": Post.objects.filter(title__icontains=data["search"])[:POST_PER_PAGE]}

    # Render HTML page and send to client
    self.send_html({
        "selector": "#all-posts",
        "html": render_to_string("components/all_posts/list.html", context),
    })
