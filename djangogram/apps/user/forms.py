from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        label='Username:',
        help_text='Last Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username...',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        required=True,
        label='Password:',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password...',
            'class': 'form-control'
        })
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username...',
            'class': 'form-control'
        })
    )
    first_name = forms.CharField(
        required=True,
        label='First name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter first name...',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        required=True,
        label='Last name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter last name...',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter email...',
            'class': 'form-control',
            'type': 'email'
        })
    )
    password1 = forms.CharField(
        required=True,
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Enter password',
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        required=True,
        label='Repeat password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Repeat password...',
            'class': 'form-control'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'bio', 'avatar']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'bio': 'Bio',
            'avatar': 'Avatar'
        }
        help_texts = {
            "avatar": 'Avatar can support only image file types'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name...', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name...', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Enter bio...', 'class': 'form-control', 'rows': 5}),
            'avatar': forms.FileInput(attrs={'placeholder': 'Select avatar...', 'type': 'file'})
        }