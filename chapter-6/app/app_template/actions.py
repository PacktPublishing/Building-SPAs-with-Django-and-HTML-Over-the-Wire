from .forms import LoginForm, SignupForm
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from django.urls import reverse
from channels.auth import login, logout
from django.contrib.auth.models import User


def send_page(self, page):
    """Render HTML and send page to client"""

    # Prepare context data for page
    context = {}
    match page:
        case "login":
            context = {"form": LoginForm()}
        case "signup":
            context = {"form": SignupForm()}

    # Add user to context if logged in
    if "user" in self.scope:
        context.update({ "user": self.scope["user"]})
    context.update({"active_nav": page})

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


def signup(self, data):
    """Sign up user"""
    form = SignupForm(data)
    if form.is_valid() and data["password"] == data["password_confirm"]:
        # Create user
        user = User.objects.create_user(data["username"], data["email"], data["password"])
        user.is_active = True
        user.save()
        # Login user
        async_to_sync(login)(self.scope, user)
        self.scope["session"].save()
        # Redirect to profile page
        send_page(self, "profile")
    else:
        # Send form errors
        self.send_html({
            "selector": "#main",
            "html": render_to_string("pages/signup.html", {"form": form}),
            "append": False,
            "url": reverse("signup")
        })

def logout(self):
    """Log out user"""
    async_to_sync(logout)(self.scope)
    self.scope["session"].save()
    send_page(self, "login")