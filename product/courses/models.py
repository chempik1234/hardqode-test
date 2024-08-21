from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from users.models import Subscription


User = get_user_model()


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )

    price = models.IntegerField(
        verbose_name="Цена",
        null=False,
        validators=[MinValueValidator(0)]
    )

    @property
    def is_available_for_user(self, user):
        if isinstance(user, User):
            return Subscription.objects.filter(user=user, course=self).exists()
        raise TypeError("user must be an instance of user model")

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=False,
        related_name="lessons",
        verbose_name="Курс",
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(
        max_length=250,
        null=False,
        validators=[MinLengthValidator(1)],
        verbose_name="Название группы"
    )
    course = models.ForeignKey(
        Course,
        related_name="groups",
        verbose_name="Курс",
        on_delete=models.CASCADE,
        null=False
    )
    students = models.ManyToManyField(
        User,
        related_name='course_groups',
        verbose_name="Студенты"
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
