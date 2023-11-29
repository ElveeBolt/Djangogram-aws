from django.urls import path
from .views import PostListView, PostView, PostCreateView, PostUpdateView, PostDeleteView, PostCommentDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('<int:pk>', PostView.as_view(), name='post'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('comments/<int:pk>/delete', PostCommentDeleteView.as_view(), name='comment-delete'),
]