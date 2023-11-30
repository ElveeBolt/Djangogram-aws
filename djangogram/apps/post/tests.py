from django.core.files.uploadedfile import SimpleUploadedFile
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

    def test_create_post(self):
        self.login()
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x02\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x02\x00\x01\x00\x00\x02\x02\x0c\x0a\x00\x3b',
            content_type='image/jpeg'
        )
        data = {'title': 'Test Post', 'description': 'This is a test post', 'tags': 'test, post', 'image': image_file}
        self.client.post('/posts/create/', data=data)
        post = Post.objects.get(title='Test Post')
        self.assertEqual(post.title, 'Test Post')

    def test_update_post(self):
        self.login()
        response = self.client.get(f'/posts/{self.post.pk}/update')
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        self.login()
        self.client.delete(f'/posts/{self.post.pk}/delete')
        post = Post.objects.all()
        self.assertEqual(post.count(), 0)

    def test_post_like(self):
        self.login()
        self.client.post(f'/posts/{self.post.pk}/like', data={'post_id': self.post.pk})
        self.assertEqual(self.post.number_of_likes(), 1)


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
