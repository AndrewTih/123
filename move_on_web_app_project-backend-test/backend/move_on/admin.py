from django.contrib import admin
from .models import User, Walk, Task, Statistics, DailyBonus, Referral, WalkSession, AnomalyLog, Donation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Администрирование модели пользователя.
    """
    list_display = ('telegram_id', 'username', 'energy', 'points',
                    'daily_streak', 'is_active', 'is_scam', 'is_fake', 'created_at')
    search_fields = ('telegram_id', 'username', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_scam', 'is_fake', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Walk)
class WalkAdmin(admin.ModelAdmin):
    """
    Администрирование модели прогулок.
    """
    list_display = ('id', 'user', 'start_time', 'end_time', 'steps',
                    'distance', 'avg_speed', 'reward', 'is_valid', 'is_lucky_walk')
    search_fields = ('user__telegram_id',)
    list_filter = ('is_valid', 'is_lucky_walk', 'start_time')
    ordering = ('-start_time',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'task_type', 'is_active', 'start_date', 'end_date')
    list_filter = ('task_type', 'is_active')


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    """
    Администрирование модели статистики.
    """
    list_display = ('user', 'total_steps', 'total_distance', 'total_rewards')
    search_fields = ('user__telegram_id',)
    ordering = ('user__telegram_id',)


@admin.register(DailyBonus)
class DailyBonusAdmin(admin.ModelAdmin):
    """
    Администрирование модели ежедневного бонуса.
    """
    list_display = ('user', 'streak', 'max_streak', 'last_claim_date')
    search_fields = ('user__telegram_id',)
    ordering = ('-streak',)


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """
    Администрирование модели рефералов.
    """
    list_display = ('user', 'invited_by', 'reward_percentage', 'total_rewards', 'total_invited')
    search_fields = ('user__telegram_id', 'invited_by__telegram_id')
    ordering = ('-total_rewards',)


@admin.register(WalkSession)
class WalkSessionAdmin(admin.ModelAdmin):
    """
    Администрирование модели активных сессий прогулок.
    """
    list_display = ('user', 'start_time', 'steps', 'distance', 'avg_speed', 'pattern')
    search_fields = ('user__telegram_id',)
    ordering = ('-start_time',)


@admin.register(AnomalyLog)
class AnomalyLogAdmin(admin.ModelAdmin):
    """
    Администрирование модели логов аномалий.
    """
    list_display = ('user', 'description', 'created_at')
    search_fields = ('user__telegram_id',)
    ordering = ('-created_at',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """
    Администрирование модели пожертвований.
    """
    list_display = ('user', 'stars_bought', 'amount_paid', 'created_at')
    search_fields = ('user__telegram_id',)
    ordering = ('-created_at',)
