from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(CustomUser, null=False, on_delete=models.CASCADE, related_name="balance")
    balance = models.IntegerField(null=False, validators=[MinValueValidator(0)], default=1000)

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    course = models.ForeignKey(
        'courses.Course',
        null=False,
        verbose_name="Курс",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        null=False,
        verbose_name="Пользователь",
        on_delete=models.CASCADE
    )
    subscription_date = models.DateTimeField(
        null=False,
        auto_created=True,
        auto_now=True,
        verbose_name="Дата подписки"
    )
    # course_accessible = models.BooleanField(
    #     default=False,
    #     null=False,
    #     verbose_name="Курс доступен"
    # )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

