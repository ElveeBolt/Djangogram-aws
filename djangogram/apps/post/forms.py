from django import forms
from taggit.forms import TagWidget

from .models import Post, Comment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    needs_multipart_form = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter title...',
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter comment...',
                    'class': 'form-control',
                    'rows': 5
                }
            ),
            'tags': TagWidget(
                attrs={
                    'placeholder': 'Enter tags...',
                    'class': 'form-control'
                }
            ),
        }


class PostImageForm(PostForm):
    image = MultipleFileField(
        label='Images',
        widget=MultipleFileInput(
            attrs={
                'placeholder': 'Enter file...',
                'class': 'form-control-file',
                'multiple': True
            }
        )
    )

    class Meta(PostForm.Meta):
        fields = PostForm.Meta.fields + ['image', ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            'comment': 'Comment'
        }
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Enter comment...',
                    'class': 'form-control',
                    'rows': 5
                }
            )
        }
