import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Comment, Follow, Group, Post, User

from yatube.settings import QUANTITY

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


INDEX = reverse('posts:index')
INDEX_FOLLOW = reverse('posts:follow_index')
SLUG = 'test_slug'
GROUP = reverse(
    'posts:group_list',
    kwargs={'any_slug': SLUG}
)
SLUG_2 = 'test_slug2'
GROUP_2 = reverse(
    'posts:group_list',
    kwargs={'any_slug': SLUG_2}
)
USER_NAME = 'auth'
USER_NAME_2 = 'man'
USER_NAME_3 = 'another'
PROFILE = reverse('posts:profile', args={USER_NAME})
POST_CREATE = reverse('posts:post_create')
SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
UPLOADED = SimpleUploadedFile(
    name='small.gif',
    content=SMALL_GIF,
    content_type='image/gif'
)


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(USER_NAME)
        cls.user_follow = User.objects.create_user(USER_NAME_2)
        cls.user_another = User.objects.create_user(USER_NAME_3)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=SLUG,
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа2',
            slug=SLUG_2,
            description='Тестовое описание2',
        )
        Follow.objects.create(
            user=cls.user_follow,
            author=cls.user,
        )
        posts_all = []
        for i in range(1, 15):
            posts_all.append(
                Post(
                    id=f'{i}',
                    text=f'Тестовая запись поста {i}',
                    author=cls.user,
                    group=cls.group,
                    image=UPLOADED,
                )
            )
        cls.post = Post.objects.bulk_create(posts_all)
        cls.POST_DETAIL = reverse('posts:post_detail', args=[cls.post[0].id])
        cls.POST_EDIT = reverse('posts:post_edit', args=[cls.post[0].id])
        cls.FOLLOW_PAGE = reverse(
            'posts:profile_follow', args={USER_NAME}
        )
        cls.UNFOLLOW_PAGE = reverse(
            'posts:profile_unfollow', args={USER_NAME}
        )
        cls.post = Comment.objects.create(
            author=cls.user,
            text='Первый на!',
            post=cls.post[0],
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.follower_client = Client()
        self.follower_client.force_login(self.user_follow)
        self.another_client = Client()
        self.another_client.force_login(self.user_another)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            INDEX: 'posts/index.html',
            GROUP: 'posts/group_list.html',
            PROFILE: 'posts/profile.html',
            self.POST_DETAIL: 'posts/post_detail.html',
            self.POST_EDIT: 'posts/create.html',
            POST_CREATE: 'posts/create.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(INDEX)
        first_object = response.context["page_obj"][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, f'{post_text_0}')
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_group_0, 'Тестовая группа')
        self.assertEqual(post_image_0, f'{post_image_0}')

    def test_paginator_index(self):
        response = self.client.get(INDEX)
        self.assertEqual(len(response.context['page_obj']), QUANTITY)

    def test_paginator_index_second(self):
        response = self.client.get(INDEX + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_group_list_page_show_correct_context(self):
        response = self.authorized_client.get(GROUP)
        first_object = response.context["page_obj"][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, f'{post_text_0}')
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_group_0, 'Тестовая группа')
        self.assertEqual(post_image_0, f'{post_image_0}')

    def test_paginator_group_list(self):
        response = self.client.get(GROUP)
        self.assertEqual(len(response.context['page_obj']), QUANTITY)

    def test_paginator_group_list_second(self):
        response = self.client.get(GROUP + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(PROFILE)
        first_object = response.context["page_obj"][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, f'{post_text_0}')
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_group_0, 'Тестовая группа')
        self.assertEqual(post_image_0, f'{post_image_0}')

    def test_paginator_profile(self):
        response = self.client.get(PROFILE)
        self.assertEqual(len(response.context['page_obj']), QUANTITY)

    def test_paginator_profile_second(self):
        response = (
            self.client.get(PROFILE + '?page=2')
        )
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_post_detail_page_show_correct_context(self):
        response = self.authorized_client.get(self.POST_DETAIL)
        first_object = response.context["post_item"]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, f'{post_text_0}')
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_group_0, 'Тестовая группа')
        self.assertEqual(post_image_0, f'{post_image_0}')

    def test_post_edit_page_show_correct_context(self):
        response = self.authorized_client.get(self.POST_EDIT)
        first_object = response.context["post_item"]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, f'{post_text_0}')
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_group_0, 'Тестовая группа')

    def test_post_create_show_correct_context(self):
        response = self.authorized_client.get(POST_CREATE)
        form_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_create_with_group_show_correct(self):
        pages_temp = [
            INDEX,
            GROUP,
            PROFILE
        ]
        for value in pages_temp:
            with self.subTest(inverse=value):
                response = self.authorized_client.get(value)
                first_object = response.context["page_obj"][0]
                self.assertEqual(first_object, first_object)

    def test_post_create_no_group(self):
        response = self.authorized_client.get(GROUP_2)
        post_count = len(response.context['page_obj'])
        self.assertEqual(post_count, 0)

    def test_comment_show(self):
        response = self.authorized_client.get(self.POST_DETAIL)
        object = response.context['post_item'].comments.all()
        comment = object[0]
        self.assertEqual(comment.text, 'Первый на!')

    def test_cache(self):
        post = Post.objects.create(
            author=self.user,
            text='Проверка кэша',
        )
        response = self.authorized_client.get(INDEX)
        cache_1 = response.content
        post.delete()
        response = self.authorized_client.get(INDEX)
        cache_2 = response.content
        response = self.authorized_client.get(INDEX)
        self.assertEqual(cache_1, cache_2)
        cache.clear()
        cache_3 = self.authorized_client.get(INDEX)
        self.assertNotEqual(cache_3, response.content)

    def test_follow(self):
        self.follower_client.get(self.FOLLOW_PAGE)
        self.assertTrue(Follow.objects.filter(
            user=self.user_follow, author=self.user).exists())

    def test_unfollow(self):
        self.follower_client.get(self.UNFOLLOW_PAGE)
        self.assertTrue(Follow.objects.filter(
            user=self.user_follow, author=self.user).exists())

    def test_follower_see_new_post(self):
        new_post = Post.objects.create(
            author=self.user,
            text="Текст нового поста")
        response = self.follower_client.get(self.FOLLOW_PAGE)
        response = self.follower_client.get(INDEX_FOLLOW)
        self.assertIn(new_post, response.context['page_obj'].object_list)

    def test_not_follower_dont_see_new_post(self):
        new_post = Post.objects.create(
            author=self.user,
            text="Текст нового поста")
        response = self.another_client.get(INDEX_FOLLOW)
        self.assertNotIn(new_post, response.context['page_obj'].object_list)
