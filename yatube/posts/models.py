from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField("Название группы", max_length=200)
    slug = models.SlugField("Адрес", unique=True)
    description = models.TextField("Описание")

    class Meta:
        verbose_name_plural = "Группа"

    def __str__(self) -> str:
        return self.title


class Post(CreatedModel):
    text = models.TextField(
        "Текст поста",
        help_text="Введите текст поста"
    )
    group = models.ForeignKey(
        Group,
        related_name="groups_name",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Группа",
        help_text="Группа, к которой будет относиться пост"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    image = models.ImageField(
        "Картинка",
        upload_to='posts/',
        blank=True
    )

    class Meta:
        verbose_name_plural = "Посты"
        # Я видимо не правильно понял про рефакторинг
        # с моделью CreatedModel из core,
        # там указывал ordering = ['-pub_date'] и не проверил, 
        # а он оказывается не работает, думал раз там мы указали,
        # то здесь надо удалить. А у меняж ведь и тест не назодил пост
        # пришлось в тесте искать его на второй странице, 
        # я тогда этому не придал значение.Вернул обратно
        ordering = ("-pub_date",)

    def __str__(self) -> str:
        return self.text[:15]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(
        "текст комментария",
        help_text="Введите текст комментария"
    )

    def __str__(self) -> str:
        return self.text[0:15]

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                name="unique_follower",
                fields=["user", "author"],
            ),
            models.CheckConstraint(
                name="not_self_follow",
                check=~models.Q(user=models.F("author")),
            ),
        ]
