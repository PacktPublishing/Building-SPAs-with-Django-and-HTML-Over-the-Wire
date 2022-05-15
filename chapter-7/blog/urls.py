from django.contrib import admin
from django.urls import path
from app.website import views, feed

urlpatterns = [
    path("", views.all_posts, name="all posts"),
    path("article/<slug:slug>/", views.single_post, name="single post"),
    path("about-us/", views.about, name="about us"),
    path("feed/", feed.LatestEntriesFeed(), name="feed"),
    path("admin/", admin.site.urls),
]

handler404 = "app.website.views.page_not_found"
