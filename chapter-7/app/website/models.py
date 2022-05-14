from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def summary(self):
        return self.content[:100] + "..."

    def get_absolute_url(self):
        return reverse("single post", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=20)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
