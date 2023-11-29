from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_active = models.BooleanField(default=False, verbose_name='Is active')
    avatar = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Avatar')
    bio = models.TextField(null=True, blank=True, verbose_name='Bio')

    def __str__(self):
        return self.username