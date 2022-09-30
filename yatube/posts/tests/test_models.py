from django.test import TestCase

from ..models import Comment, Follow, Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='auth')
        cls.user_follower = User.objects.create_user(username='man')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Тестовый пост',
        )
        cls.comment = Comment.objects.create(
            author=cls.user_follower,
            text='Тестовый комментарий',
            post=cls.post,
        )
        cls.follow = Follow.objects.create(
            user=cls.user_follower,
            author=cls.user_author,
        )

    def test_model_post_have_correct_object_names(self):
        post = PostModelTest.post
        object_name_post = self.post.text[:15]
        self.assertEqual(object_name_post, str(post))

    def test_model_group_have_correct_object_names(self):
        object_name_group = self.group.title
        self.assertEqual(object_name_group, str(self.group.title))
    
    def test_comment_have_correct_object_name(self):
        object_name_comment = self.comment.text[:15]
        self.assertEqual(object_name_comment, str(self.comment))

    def test_verbose_name(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected_value in field_verboses.items():
            with self.subTest(field=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected_value)

    def test_help_text(self):
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for value, expected_value in field_help_texts.items():
            with self.subTest(field=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected_value)
