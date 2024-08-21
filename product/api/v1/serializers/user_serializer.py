from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    balance = serializers.SerializerMethodField(read_only=True)

    def get_balance(self, obj) -> int:
        return obj.balance.balance

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'balance',)
        model = User


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    # TODO

    class Meta:
        model = Subscription
        fields = (
            # TODO
        )
