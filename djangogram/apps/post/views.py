from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.conf import settings

from .models import Post, Comment
from .forms import PostForm, CommentForm, PostImageFormSet, PostImageUpdateFormSet


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
    form_class = PostForm
    success_url = reverse_lazy('posts')
    extra_context = {
        'title': 'Create post',
        'subtitle': 'Create your post in Djangogram'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_images'] = PostImageFormSet()
        return context

    def form_valid(self, form):
        form_img = PostImageFormSet(self.request.POST, self.request.FILES)
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if form_img.is_valid():
                form_img.instance = self.object
                form_img.save()

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
        context['form_images'] = PostImageUpdateFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        form_img = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if form_img.is_valid():
                form_img.instance = self.object
                form_img.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})


class PostLikeView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=request.POST.get('post_id'))

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return redirect('post', pk=post.pk)


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts')
    success_message = 'Your post was successfully deleted'


class PostCommentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Comment
    success_message = 'Your comment was successfully deleted'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.object.post.pk})