from django.db import models
from django.contrib.auth.models import User



class Client(models.Model):
    """
    Clients for users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Room(models.Model):
    """
    Rooms for users
    """
    client = models.ManyToManyField(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)

    def __str__(self):
        return self.id
