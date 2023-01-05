from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    facebook_id = models.CharField(max_length=255, null=True)
    facebook_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username
