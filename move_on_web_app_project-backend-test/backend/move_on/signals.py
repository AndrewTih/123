from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Walk, Statistics
from django.db.models import Sum
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Walk)
def update_global_statistics(sender, instance, **kwargs):
    """
    Пересчёт глобальной статистики после сохранения новой прогулки.
    """
    stats = Walk.objects.aggregate(
        total_steps=Sum('steps'),
        total_distance=Sum('distance'),
        total_rewards=Sum('reward'),
    )
    logger.info(f"Обновлена глобальная статистика: {stats}")
