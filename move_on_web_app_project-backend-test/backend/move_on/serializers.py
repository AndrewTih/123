from rest_framework import serializers
from .models import User, Walk, Task, Statistics, DailyBonus, Referral, WalkSession, AnomalyLog


class UserStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ['total_steps', 'total_distance', 'total_rewards']


class UserSerializer(serializers.ModelSerializer):
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'telegram_id', 'username', 'first_name', 'last_name',
            'energy', 'points', 'endurance_level', 'efficiency_level', 'luck_level',
            'upgrade_points', 'daily_streak', 'max_daily_streak', 'last_login_date',
            'referral_bonus_percentage', 'is_scam', 'is_fake', 'is_active',
            'ton_wallet', 'created_at', 'updated_at', 'statistics'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_statistics(self, obj):
        stats = obj.statistics
        return StatisticsSerializer(stats).data if stats else None


class WalkSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Walk
        fields = [
            'id', 'user', 'start_time', 'end_time', 'steps', 'distance',
            'avg_speed', 'reward', 'is_lucky_walk', 'is_valid',
            'efficiency_multiplier', 'bonus_streak', 'is_interrupted', 'created_at'
        ]
        read_only_fields = ['reward', 'is_valid', 'created_at']


class WalkSessionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = WalkSession
        fields = [
            'id', 'user', 'start_time', 'steps', 'distance', 'avg_speed',
            'last_step_time', 'last_latitude', 'last_longitude',
            'data_window', 'pattern'
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'reward',
            'difficulty',
            'task_type',
            'start_date',
            'end_date',
            'is_active',
        ]


class StatisticsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Statistics
        fields = [
            'id', 'user', 'total_steps', 'total_distance', 'total_rewards'
        ]


class DailyBonusSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = DailyBonus
        fields = ['id', 'user', 'streak', 'max_streak', 'last_claim_date']


class ReferralSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    invited_by = serializers.StringRelatedField()

    class Meta:
        model = Referral
        fields = [
            'id', 'user', 'invited_by', 'reward_percentage',
            'total_rewards', 'total_invited'
        ]


class AnomalyLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = AnomalyLog
        fields = ['id', 'user', 'description', 'created_at']
        read_only_fields = ['created_at']


class CompleteTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=True, help_text="ID задачи для завершения")
    telegram_id = serializers.IntegerField(required=True, help_text="Telegram ID пользователя")