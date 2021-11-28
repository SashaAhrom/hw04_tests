import base64

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import User


class UsersViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='userman',
                                            password='fdijsojspH12m',
                                            email='idoaoavnh@gmail.com')

    def setUp(self):
        self.user_b64 = base64.b64encode(f'{UsersViewsTests.user.id}'.encode())
        self.token = PasswordResetTokenGenerator().make_token(
            UsersViewsTests.user)
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(UsersViewsTests.user)

    def test_pages_uses_correct_namespase_name(self):
        """The template uses the correct namespase:name."""
        templates_page_names = {
            'users/signup.html': reverse('users:signup'),
            'users/login.html': reverse('users:login'),
            'users/password_change_form.html': reverse(
                'users:password_change_form'),
            'users/password_change_done.html': reverse(
                'users:password_change_done'),
            'users/password_reset_form.html': reverse(
                'users:password_reset_form'),
            'users/password_reset_done.html': reverse(
                'users:password_reset_done'),
            'users/password_reset_confirm.html': reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': self.user_b64,
                        'token': 'set-password'}),
            'users/password_reset_complete.html': reverse(
                'users:password_reset_complete'),
            'users/logged_out.html': reverse('users:logout'),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_exist_form(self):
        """Form submission validation."""
        response = self.guest_client.get(reverse('users:signup'))
        self.assertIsNotNone(response.context['form'])
