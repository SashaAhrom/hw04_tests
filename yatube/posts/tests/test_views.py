from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
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
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsURLTests.user)

    def test_pages_uses_correct_namespase_name(self):
        """The template uses the correct namespase:name."""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'something_slug'}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'userman'}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': '1'}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': '1'}):
                'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_paginator_pages_contains_correct_context(self):
        """Check the paginator and correctly weld the context."""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'something_slug'}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'userman'}):
                'posts/profile.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), 10)
                first_object = response.context['page_obj'][0]
                post_text_0 = first_object.text
                post_author_0 = first_object.author.username
                post_group_0 = first_object.group.title
                self.assertEqual(post_text_0, 'Тестовая группа14')
                self.assertEqual(post_author_0, 'userman')
                self.assertEqual(post_group_0, 'Тестовая группа')
            with self.subTest(template=template + '?page=2'):
                response = self.authorized_client.get(reverse_name + '?page=2')
                if template == 'posts/group_list.html':
                    self.assertEqual(len(response.context['page_obj']), 4)
                else:
                    self.assertEqual(len(response.context['page_obj']), 5)

    def test_create_edit_pages_show_correct_context(self):
        """Check form fields."""
        templates_page_names = {
            reverse('posts:post_edit', kwargs={'post_id': '1'}):
                'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                form_fields = {
                    'text': forms.fields.CharField,
                    'group': forms.models.ModelChoiceField,
                }
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    response = self.authorized_client.get(reverse_name)
                    form_field = response.context['form'].fields[value]
                    self.assertIsInstance(form_field, expected)

    def test_post_detail_edit_pages_show_correct_context(self):
        """The post_detail and post_edit templates
        are well-formed with the correct context."""
        templates_page_names = {
            reverse('posts:post_detail', kwargs={'post_id': '1'}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': '1'}):
                'posts/create_post.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(response.context['post'].
                                 author.username, 'userman')
                self.assertEqual(response.context['post'].
                                 text, 'Тестовая группа0')
                self.assertEqual(response.context['post'].group, None)
