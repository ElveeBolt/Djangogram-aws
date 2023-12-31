from django.contrib import admin
from .models import Post, PostImage, Comment


class PostImageAdminInline(admin.StackedInline):
    model = PostImage
    extra = 0
    readonly_fields = ('image_preview',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = (PostImageAdminInline,)


class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image', 'thumbnail')
    readonly_fields = ('image_preview',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment')


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Comment, CommentAdmin)