from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PostQuerySet(models.QuerySet):
    def with_category(self):
        return self.select_related('category')


class PublishedModel(models.Model):
    """Абстрактная модель. Добавляет флаг is_published и created_at."""

    is_published = models.BooleanField(
        verbose_name='Опубликовано', default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.')

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True


class Location(PublishedModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

        def __str__(self):
            return self.name


class Category(PublishedModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL;'
            ' разрешены символы латиницы, цифры, дефис и подчёркивание.'))

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

        def __str__(self):
            return self.title


class Post(PublishedModel):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — можно'
                   ' делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория', related_name='posts'
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

        def __str__(self):
            return self.title
