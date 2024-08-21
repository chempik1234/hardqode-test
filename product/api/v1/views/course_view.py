from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def available_for_purchase(self, request):
        """Получение доступных курсов."""

        user = request.user
        # courses = self.get_queryset().exclude(students_purchased=user).filter(price__lte=user.balance.balance)
        """
        Что такое флаг доступности? Что он должен определять?
        Он должен быть True и до оплаты, и до зачисления, и после зачисления, зачем он тогда нужен?
        """
        serializer = self.get_serializer_class()(courses, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        course_to_buy = self.get_queryset().filter(pk=pk)
        if course_to_buy.exists():
            course_to_buy = course_to_buy.first()
            current_user = request.user
            enough_balance = course_to_buy.price <= current_user.balance.balance
            already_available = course_to_buy.is_available_for_user(current_user)
            if enough_balance and not already_available:
                with transaction.atomic():
                    new_subscription = Subscription()
                    new_subscription.course = course_to_buy
                    new_subscription.user = current_user

                    current_user.balance.balance -= course_to_buy.price

                    current_user.balance.save()
                    new_subscription.save()

                return Response(
                    data={"detail": f"You ({current_user}) successfully bought a course ({course_to_buy})"},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    data={"detail": f"This course ({course_to_buy}) isn't available for purchase"
                                    f" ({'already available' if already_available else 'not enough bonuses'})"},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
        else:
            return Response(
                data={"detail": f"Course with pk {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
