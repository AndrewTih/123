import random
from scipy.signal import butter, filtfilt, find_peaks
from haversine import haversine, Unit
import numpy as np


def calculate_reward(distance, steps, avg_speed, user):
    """
    Расчёт награды за прогулку.

    Аргументы:
    - distance: Пройденная дистанция (км).
    - steps: Количество шагов.
    - avg_speed: Средняя скорость (км/ч).
    - user: Экземпляр пользователя для учёта его навыков и бонусов.

    Возвращает:
    - Общую награду с учётом всех факторов.
    """
    # Основные множители
    distance_factor = distance * 10
    step_factor = steps / 100
    speed_factor = 1 if 5 <= avg_speed <= 12 else 0.7

    # Дополнительные бонусы
    efficiency_bonus = 1 + (user.efficiency_level * 0.3)  # 30% за уровень эффективности
    endurance_bonus = 1 + (user.endurance_level * 0.6)  # 60% за уровень выносливости
    streak_bonus = 1 + (user.daily_streak * 0.05)  # 5% за день стрика, максимум x2
    streak_bonus = min(streak_bonus, 2)  # Ограничение стрика

    # Базовая награда
    base_reward = (distance_factor + step_factor) * speed_factor

    # Учитываем все бонусы
    total_reward = base_reward * efficiency_bonus * endurance_bonus * streak_bonus

    # Удачная прогулка
    luck_chance = user.luck_level * 5  # 5% за уровень удачи
    if random.randint(1, 100) <= luck_chance:  # Если выпадет удача
        total_reward *= random.choice([1.5, 2])  # Умножаем на x1.5 или x2

    return round(total_reward, 2)


def calculate_distance(lat1, lon1, lat2, lon2):
    return haversine((lat1, lon1), (lat2, lon2), unit=Unit.METERS)

# Фильтр скользящего среднего нашёл на аутсорсе
def moving_average(data, window_size=5):
    if len(data) < window_size:
        return []
    return [sum(data[i:i+window_size]) / window_size for i in range(len(data) - window_size + 1)]


def butter_lowpass_filter(data, cutoff=3.0, fs=50.0, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)


def detect_steps(data, min_freq=0.5, max_freq=3.0, sampling_rate=50):
    threshold = np.std(data) * 1.5
    min_distance = int(sampling_rate / max_freq)
    peaks, _ = find_peaks(data, height=threshold, distance=min_distance)
    return len(peaks)