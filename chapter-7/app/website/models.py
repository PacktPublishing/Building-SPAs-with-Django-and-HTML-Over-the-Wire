from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=20)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name