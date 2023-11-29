from django import forms
from django.forms import inlineformset_factory

from .models import Post, Comment, PostImage


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'tags': 'Tags'
        }
        help_texts = {
            'description': 'A detailed description of post',
            'tags': 'A comma-separated list of tags'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title...', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter comment...', 'class': 'form-control', 'rows': 5}),
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags...', 'class': 'form-control'}),
        }


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']
        labels = {
            'image': 'Image',
        }
        widgets = {
            'image': forms.FileInput(attrs={'placeholder': 'Enter file...', 'class': 'form-control-file', 'type': 'file'})
        }


PostImageFormSet = inlineformset_factory(
    parent_model=Post,
    model=PostImage,
    form=PostImageForm,
    fields=['image'],
    extra=3,
    can_delete=True
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            'comment': 'Comment'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Enter comment...', 'class': 'form-control', 'rows': 5})
        }
