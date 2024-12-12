import logging
from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import WalkSession, Walk
from .utils import calculate_reward

logger = logging.getLogger(__name__)


@shared_task
def auto_complete_walks():
    """
    Проверяем и завершаем прогулки, которые нужно завершить
    """
    sessions = WalkSession.objects.all()
    for session in sessions:
        elapsed_time = now() - session.last_step_time if session.last_step_time else None

        if session.last_step_time and elapsed_time:
            if elapsed_time.total_seconds() > 600: 
                logger.info(f'Завершаем прогулку для пользователя {session.user.telegram_id} по истечению времени.')
                reward = calculate_reward(session.distance, session.steps, session.avg_speed, session.user)

                Walk.objects.create(
                    user=session.user,
                    start_time=session.start_time,
                    end_time=now(),
                    steps=session.steps,
                    distance=session.distance,
                    avg_speed=session.avg_speed,
                    reward=reward,
                    is_interrupted=True,
                )

                session.delete()
    return f'{sessions.count()} прогулок проверено и завершено.'
