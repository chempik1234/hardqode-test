from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Balance

from api.v1.serializers.user_serializer import CustomUserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options", "post"]
    permission_classes = (permissions.IsAdminUser,)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAdminUser,)
    )
    def add_balance(self, request, pk):
        add_value = request.data.get('add_value')
        if not isinstance(add_value, int):
            return Response({"detail": "add_value must be an integer!"}, status=status.HTTP_400_BAD_REQUEST)
        elif add_value < 0:
            return Response({"detail": "add_value must be non-negative!"}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_queryset().objects.filter(pk=pk)
        if not user.exists():
            return Response({"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        user.balance.balance += add_value
        user.balance.save()
        return Response(self.serializer_class()(user).data, status=status.HTTP_201_CREATED)


# class BalanceViewSet(viewsets.ModelViewSet):
#     queryset = Balance.objects.all()