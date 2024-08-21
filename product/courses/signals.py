from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:  # Пользователь распределяется только при создании новой подписки
        current_course = instance.course
        current_user = instance.user
        groups_queryset = Group.objects.filter(course=current_course)
        groups_count = groups_queryset.count()
        if groups_count < 10:  # групп должно быть 10 и если их меньше надо создать ещё одну для пользователя
            new_group = Group()  # так будет сначала 10 групп по 1 пользователю, затем в них распределят остальных
            new_group.course = current_course  # создавать 10 пустых групп для <10 пользователей нет смысла, так что
            new_group.students.add(current_user)  # создаём по 1
            new_group.save()
        else:  # если групп уже 10, то всё отлично, добавим новичка в самую маленькую
            smallest_group = groups_queryset.annotate(num_students=Count('students')).order_by('num_students').first()
            smallest_group.students.add(current_user)
            smallest_group.save()
        # если >10, то всё, приехали

