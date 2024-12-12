import uuid
from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class User(models.Model):
    """
        Модель пользователя, представляющая данные о пользователе приложения.

        Поля:
        - telegram_id: Уникальный идентификатор Telegram-пользователя (обязательное поле).
        - username: Имя пользователя в Telegram (опционально, может быть пустым).
        - first_name: Имя пользователя (опционально, может быть пустым).
        - last_name: Фамилия пользователя (опционально, может быть пустой).

        Энергия и очки:
        - energy: Текущая энергия пользователя (по умолчанию 100), уменьшается при прогулках.
        - points: Количество очков пользователя, которые он зарабатывает за прогулки и выполнение заданий (по умолчанию 0).

        Навыки:
        - endurance_level: Уровень выносливости пользователя, влияет на скорость расхода энергии (по умолчанию 0).
        - efficiency_level: Уровень эффективности, увеличивает награду за прогулки (по умолчанию 0).
        - luck_level: Уровень удачи, увеличивает вероятность "удачной прогулки" (по умолчанию 0).
        - upgrade_points: Количество очков прокачки, доступных для улучшения навыков (по умолчанию 0).

        Ежедневный стрик:
        - max_daily_streak: Максимальное количество дней подряд, когда пользователь заходил в приложение.
        - daily_streak: Текущий стрик, увеличивается при ежедневных входах.
        - last_login_date: Дата последнего входа пользователя.

        Реферальная система:
        - referral_bonus_percentage: Процент бонуса от доходов приглашённых пользователей (по умолчанию 10%).

        Вспомогательные данные:
        - is_scam: Указывает, является ли пользователь подозреваемым в мошенничестве (по умолчанию False).
        - is_fake: Указывает, является ли пользователь фейковым (по умолчанию False).
        - is_active: Статус активности пользователя (True, если пользователь может взаимодействовать с системой).
        - ton_wallet: Кошелёк пользователя в сети TON (опционально, может быть пустым).

        Системные данные:
        - created_at: Дата и время создания записи.
        - updated_at: Дата и время последнего обновления записи.

        Методы:
        - __str__: Возвращает строковое представление пользователя в формате:
          "User <telegram_id> (<username или 'No username'>)".
        """
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    energy = models.IntegerField(default=100)
    max_energy = models.IntegerField(default=100)
    last_energy_update = models.DateTimeField(auto_now_add=True)
    points = models.FloatField(default=0)
    endurance_level = models.IntegerField(default=0)
    efficiency_level = models.IntegerField(default=0)
    luck_level = models.IntegerField(default=0)
    upgrade_points = models.IntegerField(default=0)
    max_daily_streak = models.IntegerField(default=0, help_text="Максимальный достигнутый ежедневный стрик.")
    daily_streak = models.IntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)
    referral_bonus_percentage = models.FloatField(default=10)
    is_scam = models.BooleanField(default=False)
    is_fake = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, help_text="Статус активности пользователя.")
    ton_wallet = models.CharField(max_length=255, null=True, blank=True)
    referral_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, help_text="Уникальный идентификатор для реферальной программы")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User {self.telegram_id} ({self.username or 'No username'})"

    def update_energy(self):
        """
        Обновляет текущую энергию пользователя на основе времени последнего обновления.
        """
        now_time = now()
        elapsed_time = now_time - self.last_energy_update

        if elapsed_time.total_seconds() < 60 * 12:
            return

        restored_energy = int(elapsed_time.total_seconds() // (60 * 12))
        if restored_energy > 0:
            self.energy = min(100, self.energy + restored_energy)
            self.last_energy_update = now_time
            self.save()

class Walk(models.Model):
    """
        Модель прогулки, представляющая данные о конкретной сессии ходьбы пользователя.

        Поля:
        - user: Ссылка на пользователя, совершившего прогулку.
        - start_time: Время начала прогулки.
        - end_time: Время завершения прогулки.
        - steps: Количество шагов, сделанных во время прогулки.
        - distance: Пройденное расстояние.
        - avg_speed: Средняя скорость прогулки.
        - reward: Награда за прогулку.
        - is_lucky_walk: Флаг, была ли прогулка "удачной".
        - is_valid: Флаг, была ли прогулка валидной.
        - efficiency_multiplier: Множитель эффективности, влияющий на награду.
        - bonus_streak: Бонус за стрик.
        - is_interrupted: Указывает, была ли прогулка прервана.

        Системные данные:
        - created_at: Дата создания записи о прогулке.

        Методы:
        - __str__: Возвращает строковое представление прогулки.
        """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="walks")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    steps = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    avg_speed = models.FloatField(default=0)
    reward = models.FloatField(default=0)
    is_lucky_walk = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
    efficiency_multiplier = models.FloatField(default=1.0)
    bonus_streak = models.FloatField(default=1.0)
    is_interrupted = models.BooleanField(default=False, help_text="Указывает, была ли прогулка прервана пользователем до её завершения.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Walk {self.id} - User {self.user.telegram_id}"


class DailyBonus(models.Model):
    """
    Модель ежедневного бонуса и стрика.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="daily_bonus")
    streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    last_claim_date = models.DateField(null=True, blank=True)
    claimed_days = models.JSONField(default=dict)
    streak_rewards = models.JSONField(default=dict)

    def __str__(self):
        return f"DailyBonus - User {self.user.telegram_id} - Streak {self.streak}"

    def process_daily_bonus(self):
        """
        Начисляет ежедневный бонус и обновляет стрик.
        """
        today = now().date()
        if self.last_claim_date == today:
            return

        if self.last_claim_date == today - timedelta(days=1):
            self.streak += 1
        else:
            self.streak = 1

        self.max_streak = max(self.max_streak, self.streak)
        self.last_claim_date = today

        bonus = 0.05 * 100
        self.user.points += bonus
        self.claimed_days[str(today)] = {"coinsEarned": bonus, "bonusReceived": True}
        self.user.save()
        self.save()

    def process_streak_reward(self):
        """
        Начисляет бонус за стрик каждые 5 дней.
        """
        milestones = [5, 10, 15]
        rewards = self.streak_rewards
        for milestone in milestones:
            if self.streak >= milestone and str(milestone) not in rewards:
                self.user.upgrade_points += 1
                rewards[str(milestone)] = True
                self.user.save()
        self.streak_rewards = rewards
        self.save()

    def reset_streak(self):
        """
        Сбрасывает стрик и связанные данные, если пользователь пропустил день.
        """
        today = now().date()
        if self.last_claim_date != today - timedelta(days=1):
            self.streak = 0
            self.claimed_days = {}
            self.streak_rewards = {}
            self.save()


class Referral(models.Model):
    """
    Модель реферала, представляющая данные о рефералах пользователя.

    Поля:
    - user: Ссылка на пользователя, который является рефералом.
    - invited_by: Ссылка на пользователя, который пригласил этого реферала (может быть пустым, если пользователь не был приглашён).
    - reward_percentage: Процент награды для пользователя за приглашённого реферала (по умолчанию 5%).
    - total_rewards: Общая сумма наград, полученных за рефералов.
    - total_invited: Общее количество приглашённых пользователей.

    Методы:
    - __str__: Возвращает строковое представление реферала в формате:
      "Referral - User <telegram_id> invited by <invited_by_telegram_id>".
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referral")
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="invited_users")
    reward_percentage = models.FloatField(default=5)
    total_rewards = models.FloatField(default=0)
    total_invited = models.IntegerField(default=0)

    def __str__(self):
        return f"Referral - User {self.user.telegram_id} invited by {self.invited_by.telegram_id if self.invited_by else ''}"



class Task(models.Model):
    """
    Модель задания для всех пользователей.
    """
    TASK_TYPES = [
        ('daily', 'Ежедневное'),
        ('challenge', 'Челлендж'),
    ]

    name = models.CharField(max_length=255, help_text="Название задания")
    description = models.TextField(null=True, blank=True, help_text="Описание задания")
    reward = models.FloatField(default=0, help_text="Награда за выполнение задания")
    difficulty = models.IntegerField(default=1, help_text="Сложность задания (1-легко, 3-сложно)")
    task_type = models.CharField(
        max_length=20,
        choices=TASK_TYPES,
        default='daily',
        help_text="Тип задания (ежедневное, челлендж)"
    )
    start_date = models.DateField(null=True, blank=True, help_text="Дата начала действия задания")
    end_date = models.DateField(null=True, blank=True, help_text="Дата окончания действия задания")
    is_active = models.BooleanField(default=True, help_text="Активно ли задание")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания задания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата последнего обновления")

    def __str__(self):
        return f"Task {self.name} - Type: {self.task_type}"

    @property
    def is_available(self):
        """
        Проверяет, активно ли задание на текущую дату.
        """
        today = now().date()
        return self.is_active and (
            (self.start_date is None or self.start_date <= today) and
            (self.end_date is None or self.end_date >= today)
        )


class Statistics(models.Model):
    """
    Модель статистики пользователя, отслеживающая общие показатели его активности.

    Поля:
    - user: Ссылка на пользователя, к которому относится статистика (OneToOneField к модели User).
    - total_steps: Общее количество шагов, которые пользователь совершил.
    - total_distance: Общая пройденная дистанция в километрах.
    - total_rewards: Общее количество наград, которые пользователь получил.

    Методы:
    - __str__: Возвращает строковое представление статистики в формате:
      "Statistics - User <telegram_id>".
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="statistics")
    total_steps = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0)
    total_rewards = models.FloatField(default=0)

    def __str__(self):
        return f"Statistics - User {self.user.telegram_id}"


class WalkSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="walk_sessions")
    start_time = models.DateTimeField(auto_now_add=True)
    steps = models.IntegerField(default=0)
    distance = models.FloatField(default=0.0)
    avg_speed = models.FloatField(default=0.0)
    last_step_time = models.DateTimeField(null=True, blank=True)
    last_latitude = models.FloatField(null=True, blank=True)
    last_longitude = models.FloatField(null=True, blank=True)
    data_window = models.JSONField(default=list)
    pattern = models.CharField(max_length=50, default="неопределен")

    def __str__(self):
        return f"WalkSession {self.id} - User {self.user.telegram_id}"


class AnomalyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="anomalies")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Donation(models.Model):
    """
    Модель пожертвования, представляющая информацию о покупке звёзд пользователем.

    Поля:
    - user: Ссылка на пользователя, который совершил покупку (ForeignKey к модели User).
    - stars_bought: Количество звёзд, купленных пользователем.
    - amount_paid: Сумма, уплаченная пользователем за покупку (в валюте, используемой приложением).
    - created_at: Дата и время создания записи о покупке.

    Методы:
    - __str__: Возвращает строковое представление пожертвования в формате:
      "Donation - User <telegram_id>, Stars: <stars_bought>".
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    stars_bought = models.IntegerField()
    amount_paid = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation - User {self.user.telegram_id}, Stars: {self.stars_bought}"


class GlobalStatistics(models.Model):
    total_steps = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0)
    total_rewards = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
