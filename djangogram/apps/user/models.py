from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Avatar')
    bio = models.TextField(null=True, blank=True, verbose_name='Bio')

    def __str__(self):
        return self.username