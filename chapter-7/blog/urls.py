from django.contrib import admin
from django.urls import path
from app.website import views

urlpatterns = [
    path("", views.all_posts, name="all_posts"),
    path("article/<slug:slug>/", views.single, name="single"),
    path("about/", views.about, name="about"),
    path("admin/", admin.site.urls),
]

handler404 = "app.website.views.page_not_found"