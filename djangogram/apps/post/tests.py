from django.test import TestCase, Client
from apps.user.models import User
from .models import Post, Comment


# Create your tests here.
class TestCasePost(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='user', password='user')
        user.is_active = True
        user.save()

        self.post = Post.objects.create(user=user, title='Post', description='Description', tags='tag1 tag2')

    def login(self):
        self.client.login(username='user', password='user')

    def test_posts(self):
        self.login()
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.login()
        response = self.client.get(f'/posts/{self.post.pk}')
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        self.login()
        response = self.client.get(f'/posts/{self.post.pk}/update')
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        self.login()
        self.client.delete(f'/posts/{self.post.pk}/delete')
        post = Post.objects.all()
        self.assertEqual(post.count(), 0)


class TestCaseComment(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='user', password='user')
        user.is_active = True
        user.save()

        self.post = Post.objects.create(user=user, title='Post', description='Description', tags='tag1 tag2')
        self.comment = Comment.objects.create(user=user, post=self.post, comment='Comment')

    def login(self):
        self.client.login(username='user', password='user')

    def test_post_comment(self):
        self.login()
        self.client.post(f'/posts/{self.post.pk}', data={'comment': 'Comment'})
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 2)

    def test_delete_comment(self):
        self.login()
        self.client.delete(f'/posts/comments/{self.comment.pk}/delete')
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 0)