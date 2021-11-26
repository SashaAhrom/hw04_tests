from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_create_user_redirect(self):
        """Validation creates a new user when submitting 'users:signup'."""
        posts_count = User.objects.count()
        form_data = {
            'first_name': 'Johannes',
            'last_name': 'Klaebo',
            'username': 'skier',
            'email': 'Klaebo@gmai.com',
            'password1': '1234werfdsa',
            'password2': '1234werfdsa'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), posts_count + 1)
