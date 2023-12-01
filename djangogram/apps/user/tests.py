from django.test import TestCase, Client
from .models import User, UserFriend
from apps.post.models import Post


# Create your tests here.
class TestCaseUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.form_data = {
            'username': 'user',
            'first_name': 'User',
            'last_name': 'User',
            'email': 'user@example.com',
            'password1': 'MS91KOp_e',
            'password2': 'MS91KOp_e'
        }

    def test_login(self):
        response = self.client.post(f'/users/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.post(f'/users/signup/')
        self.assertEqual(response.status_code, 200)

    def test_user_signup_view(self):
        response = self.client.post(f'/users/signup/', data=self.form_data)
        self.assertRedirects(response, '/users/login/')

        user = User.objects.get(username='user')
        self.assertEqual(user.email, 'user@example.com')
        self.assertFalse(user.is_active)


# Create your tests here.
class TestCaseUserFriend(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='user', password='user')
        self.user.is_active = True
        self.user.save()

        self.friend = User.objects.create_user(username='user_2', password='user_2')
        self.friend.is_active = True
        self.friend.save()

        self.friend_1 = User.objects.create_user(username='user_3', password='user_3')
        self.friend_1.is_active = True
        self.friend_1.save()

        UserFriend.objects.create(from_user=self.user, to_user=self.friend)
        self.post = Post.objects.create(user=self.user, title='Post', description='Description', tags='tag1 tag2')

    def login(self):
        self.client.login(username='user', password='user')

    def test_friends(self):
        self.login()
        response = self.client.get(f'/users/friends/')
        self.assertEqual(response.status_code, 200)

    def test_add_friend(self):
        self.login()
        self.client.post(f'/users/friends/{self.friend_1.id}/action', data={'profile_id': self.friend_1.id})
        friends = UserFriend.objects.filter(from_user=self.user).count()
        self.assertEqual(friends, 2)

    def test_delete_friend(self):
        self.login()
        self.client.post(f'/users/friends/{self.friend.id}/action', data={'profile_id': self.friend.id})
        friends = UserFriend.objects.filter(from_user=self.user).count()
        self.assertEqual(friends, 0)
