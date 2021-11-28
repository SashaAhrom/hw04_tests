from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='userman')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='something_slug',
            description='Тестовое описание',
        )
        for i in range(15):
            if i != 0:
                cls.post = Post.objects.create(
                    author=cls.user,
                    text='Тестовая группа' + str(i),
                    group=cls.group
                )
            else:
                cls.post = Post.objects.create(
                    author=cls.user,
                    text='Тестовая группа' + str(i),
                )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.__class__.user)

    def test_create_post(self):
        """Check a new record is created in Post."""
        posts_count = Post.objects.count()
        form_data = {
            'author': self.user,
            'text': 'Новый тестовый текст ',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile',
                                               kwargs={'username': self.user}))
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        """Сhecking the editing of a record in Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Редактированный тестовый текст',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     kwargs={'post_id': self.post.pk}))
        self.assertEqual(Post.objects.count(), posts_count)
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.context['post'].text,
                         'Редактированный тестовый текст')
