from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestEntriesFeed(Feed):
    title = "My blog"
    link = "/feed/"
    description = "Updates to posts."

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return reverse("single post", kwargs={"slug": item.slug})
