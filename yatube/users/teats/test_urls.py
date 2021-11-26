import base64
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import Client, TestCase

User = get_user_model()


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='userman',
                                            password='fdijsojspH12m',
                                            email='idoaoavnh@gmail.com')

    def setUp(self):
        self.user_b64 = base64.b64encode(f'{UsersURLTests.user.id}'.encode())
        self.token = PasswordResetTokenGenerator().make_token(
            UsersURLTests.user)
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(UsersURLTests.user)

    def test_url_correct_template_status_code_unauthorized(self):
        """Checking status_code and URL-the address
        uses the appropriate template."""
        templates_url_names = {
            'users/signup.html': '/auth/signup/',
            'users/login.html': '/auth/login/',
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)
                self.assertTemplateUsed(response, template)

    def test_url_correct_template_status_code_authorized(self):
        """Checking status_code and URL-the address
        uses the appropriate template."""
        templates_url_names = {
            'users/password_reset_form.html': '/auth/password_reset/',
            'users/password_reset_done.html': '/auth/password_reset/done/',
            'users/password_change_form.html': '/auth/password_change/',
            'users/password_change_done.html': '/auth/password_change/done/',
            'users/password_reset_confirm.html':
                f'/auth/reset/{self.user_b64}/set-password/',
            'users/password_reset_complete.html': '/auth/reset/done/',
            'users/logged_out.html': '/auth/logout/',
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)
                self.assertTemplateUsed(response, template)
