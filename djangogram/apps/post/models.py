import os
import sys
from io import BytesIO

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager
from PIL import Image

from apps.user.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    title = models.CharField(null=False, max_length=255, verbose_name='Title')
    description = models.TextField(null=False, blank=True, verbose_name='Description')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='Date publish')
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-date_publish']
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'Posts'


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='images')
    # image = models.ImageField(null=False, max_length=255, upload_to='posts', verbose_name='Image')
    image = CloudinaryField('posts', null=False, max_length=255)
    # thumbnail = models.ImageField(upload_to='posts/thumbnails')
    thumbnail = CloudinaryField('posts/thumbnails')

    def __str__(self):
        return self.image.url

    def image_preview(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" />')

    image_preview.allow_tags = True
    image_preview.short_description = 'Image'

    def save(self, **kwargs):
        width = 600
        height = 600

        output_size = (width, height)
        output_thumb = BytesIO()

        img = Image.open(self.image)
        img_name = os.path.splitext(self.image.name)[0]

        if img.height > height or img.width > width:
            img.thumbnail(output_size, Image.Resampling.LANCZOS)
            img.save(output_thumb, format=img.format, quality=90)

        self.thumbnail = InMemoryUploadedFile(
            file=output_thumb,
            field_name='ImageField',
            name=f"{img_name}_thumb.{img.format}",
            content_type='image/jpeg',
            size=sys.getsizeof(output_thumb),
            charset=None
        )
        super().save()

    class Meta:
        db_table = 'post_images'
        verbose_name = 'image'
        verbose_name_plural = 'Images'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='comments')
    comment = models.TextField(null=False, blank=True, verbose_name='Comment')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='Date publish')

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'post_comments'
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'
