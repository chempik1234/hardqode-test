from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import CustomUser, Balance


@receiver(post_save, sender=CustomUser)
def post_save_custom_user(sender, instance: CustomUser, created, **kwargs):
    """
    Создание баланса для пользователя после его регистрации

    """

    if created:  # Пользователь распределяется только при создании новой подписки
        new_balance = Balance()
        new_balance.user = instance
        new_balance.balance = 1000
        new_balance.save()
