from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_alex = User.objects.create_user(username='user_alex')
        cls.user = User.objects.create_user(username='userman')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='something_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsURLTests.user)

    def test_page_not_exist(self):
        """This page does not exist."""
        response = self.guest_client.get('/strege_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_url_correct_template_status_code_unauthorized(self):
        """Checking status_code and URL-the address
        uses the appropriate template."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/something_slug/': 'posts/group_list.html',
            '/profile/userman/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)
                self.assertTemplateUsed(response, template)

    def test_url_correct_template_status_code_authorized(self):
        """Checking status_code and URL-the address
        uses the appropriate template."""
        templates_url_names = {
            '/posts/1/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)
                self.assertTemplateUsed(response, template)

    def test_create_url_redirect_anonymous_to_login(self):
        """The page / create / will redirect the anonymous user
        to the login page."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/')

    def test_posts_edit_url_redirect_authorized(self):
        """The page /posts/1/edit/ will redirect the authorized user
        to /posts/1/."""
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsURLTests.user_alex)
        response = self.authorized_client.get('/posts/1/edit/', follow=True)
        self.assertRedirects(response, '/posts/1/')
