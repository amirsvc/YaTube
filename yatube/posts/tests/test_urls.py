from django.test import Client, TestCase
from django.urls import reverse
from django.core.cache import cache

from http import HTTPStatus

from ..models import Group, Post, User


INDEX = reverse('posts:index')
SLUG = 'test_slug'
GROUP = reverse(
    'posts:group_list',
    kwargs={'any_slug': SLUG}
)
NOT_FOUD_PAGE = '/unexisting_page/'
USER_NAME = 'auth'
USER_NAME_2 = 'HasNoName'
PROFILE = reverse('posts:profile', args={USER_NAME})
POST_CREATE = reverse('posts:post_create')


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(USER_NAME)
        cls.user2 = User.objects.create_user(USER_NAME_2)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=SLUG,
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )
        cls.POST_EDIT = reverse('posts:post_edit', args=[cls.post.id])
        cls.POST_DETAIL = reverse('posts:post_detail', args=[cls.post.id])
        cls.COMMENT = reverse('posts:add_comment', args=[cls.post.id])

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user2)
        self.authorized_author = Client()
        self.authorized_author.force_login(self.user)

    def test_urls_guest(self):
        templates_url_status_guest = {
            INDEX: HTTPStatus.OK,
            GROUP: HTTPStatus.OK,
            PROFILE: HTTPStatus.OK,
            self.POST_DETAIL: HTTPStatus.OK,
            NOT_FOUD_PAGE: HTTPStatus.NOT_FOUND,
        }
        for address, url_status in templates_url_status_guest.items():
            with self.subTest(address=address):
                response = self.authorized_author.get(address)
                self.assertEqual(response.status_code, url_status)

    def test_urls_author(self):
        templates_url_status_authorized = {
            POST_CREATE: HTTPStatus.OK,
        }
        for address, url_status in templates_url_status_authorized.items():
            with self.subTest(address=address):
                response = self.authorized_author.get(address)
                self.assertEqual(response.status_code, url_status)

    def test_urls_author(self):
        templates_url_status_author = {
            self.POST_EDIT: HTTPStatus.OK,
        }
        for address, url_status in templates_url_status_author.items():
            with self.subTest(address=address):
                response = self.authorized_author.get(address)
                self.assertEqual(response.status_code, url_status)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            INDEX: 'posts/index.html',
            POST_CREATE: 'posts/create.html',
            self.POST_EDIT: 'posts/create.html',
            GROUP: 'posts/group_list.html',
            PROFILE: 'posts/profile.html',
            self.POST_DETAIL: 'posts/post_detail.html',
            NOT_FOUD_PAGE: 'core/404.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_author.get(address)
                self.assertTemplateUsed(response, template)

    def test_url_comment(self):
        response = self.guest_client.get(self.COMMENT)
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{self.post.pk}/comment/'
        )
