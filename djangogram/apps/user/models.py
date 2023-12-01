from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # avatar = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Avatar')
    avatar = CloudinaryField('users/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True, verbose_name='Bio')

    def __str__(self):
        return self.username


class UserFriend(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE, verbose_name='User')
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE, verbose_name='Friend')

    def __str__(self):
        return f'{self.from_user} => {self.to_user}'