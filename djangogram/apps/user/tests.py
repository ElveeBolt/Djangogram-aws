from django.test import TestCase, Client
from .models import User


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
