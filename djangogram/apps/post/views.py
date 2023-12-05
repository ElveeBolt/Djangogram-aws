from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.conf import settings

from .models import Post, Comment, PostImage
from .forms import PostForm, CommentForm, PostImageForm
from ..user.models import UserFriend


# Create your views here.
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'apps/post/post_list.html'
    context_object_name = 'posts'
    paginate_by = settings.PAGINATE_COUNT
    extra_context = {
        'title': 'Posts',
        'subtitle': 'List of posts'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if 'tag' in self.request.GET:
            return queryset.filter(tags__name=self.request.GET['tag'])
        return queryset


class PostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentFormView.as_view()
        return view(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'apps/post/post.html'
    context_object_name = 'post'
    extra_context = {
        'title': 'Post',
        'subtitle': 'Detailed information about the post'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object, 'user': self.request.user})
        liked = False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['number_of_likes'] = self.object.number_of_likes()
        context['post_is_liked'] = liked
        return context


class PostCommentFormView(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'apps/post/post.html'
    success_message = 'Your comment has been added successfully'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.post = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'apps/post/post_form.html'
    form_class = PostImageForm
    success_url = reverse_lazy('posts')
    extra_context = {
        'title': 'Create post',
        'subtitle': 'Create your post in Djangogram'
    }

    def post(self, request, *args, **kwargs):
        form = PostImageForm(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        if self.request.FILES:
            for file in self.request.FILES.getlist('image'):
                PostImage.objects.create(image=file, post=post)

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    template_name = 'apps/post/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('posts')
    success_message = 'Your post was successfully updated'
    extra_context = {
        'title': 'Update post',
        'subtitle': 'Update your post in Djangogram'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = PostImage.objects.filter(post=self.get_object()).all()
        return context

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})


class PostLikeView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs.get('pk'))

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            status = False
        else:
            post.likes.add(request.user)
            status = True

        return JsonResponse({
            'status': status,
            'count': post.number_of_likes()
        })


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts')
    success_message = 'Your post was successfully deleted'


class PostCommentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Comment
    success_message = 'Your comment was successfully deleted'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.object.post.pk})


class PostFriendListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'apps/post/post_list.html'
    context_object_name = 'posts'
    paginate_by = settings.PAGINATE_COUNT
    extra_context = {
        'title': 'Posts of my friends',
        'subtitle': 'List of posts'
    }

    def get_queryset(self, *args, **kwargs):
        friends = UserFriend.objects.filter(from_user=self.request.user).values_list('id', flat=True)
        return Post.objects.filter(user_id__in=friends).all()