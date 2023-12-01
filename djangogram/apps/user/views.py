from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, FormView, TemplateView
from django.contrib.auth.tokens import default_token_generator

from .models import User, UserFriend
from .forms import LoginForm, SignUpForm, UserUpdateForm
from apps.post.models import Post

from .utils import send_signup_activation_code


# Create your views here.
class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'apps/user/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'title': 'Sign in',
        'subtitle': 'To start using Djangogram features, please login',
    }


class UserSignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'apps/user/signup.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Sign up',
        'subtitle': 'To start using Djangogram features, please signup',
    }

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        send_signup_activation_code(request=self.request, user=user)
        return redirect('login')


class UserSignupVerifyView(View):
    def dispatch(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('signup-verify-success')

        return redirect('signup-verify-invalid')


class UserSignupVerifySuccessView(TemplateView):
    template_name = 'apps/user/signup_confirm_success.html'
    extra_context = {
        'title': 'Email verify',
        'subtitle': 'Sign up confirm success'
    }


class UserSignupVerifyInvalidView(TemplateView):
    template_name = 'apps/user/signup_confirm_invalid.html'
    extra_context = {
        'title': 'Email verify',
        'subtitle': 'Sign up confirm invalid'
    }


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'apps/user/user.html'
    context_object_name = 'profile'
    extra_context = {
        'title': 'User',
        'subtitle': 'Detailed information about user'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_queryset_posts()
        context['profile_if_friend'] = UserFriend.objects.filter(from_user=self.request.user, to_user=self.object).exists()
        return context

    def get_queryset_posts(self):
        return Post.objects.filter(user=self.object)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'apps/user/user_list.html'
    context_object_name = 'users'
    paginate_by = settings.PAGINATE_COUNT
    extra_context = {
        'title': 'Users',
        'subtitle': 'List of users'
    }


class UserSettingsView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = UserUpdateForm
    template_name = 'apps/user/settings.html'
    success_url = reverse_lazy('user-settings')
    success_message = 'Your profile was successfully updated'
    extra_context = {
        'title': 'User update profile',
        'subtitle': 'Update your info in profile',
    }

    def get_initial(self):
        user = self.request.user
        return {'first_name': user.first_name, 'last_name': user.last_name, 'bio': user.bio, 'avatar': user.avatar}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserFriendListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'apps/user/user_list.html'
    context_object_name = 'users'
    paginate_by = settings.PAGINATE_COUNT
    extra_context = {
        'title': 'My friends',
        'subtitle': 'List of your friends'
    }

    def get_queryset(self, **kwargs):
        friends = UserFriend.objects.filter(from_user=self.request.user).values_list('id', flat=True)
        return User.objects.filter(id__in=friends)


class UserFriendActionView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        to_user = User.objects.get(pk=request.POST.get('profile_id'))

        try:
            friend = UserFriend.objects.get(from_user=self.request.user, to_user=to_user)
            friend.delete()
        except UserFriend.DoesNotExist:
            friend = UserFriend.objects.create(from_user=self.request.user, to_user=to_user)
            print(friend)

        return redirect('user', pk=friend.to_user.pk)
