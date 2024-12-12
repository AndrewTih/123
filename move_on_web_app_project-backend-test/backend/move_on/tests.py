from django.utils.timezone import now
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Walk, Task, Statistics
from django.urls import reverse


class UserAPITestCase(APITestCase):
    def test_get_user_energy(self):
        user = User.objects.create(telegram_id=12345)
        user.energy = 100
        user.save()

        url = reverse('get_energy', args=[user.telegram_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('energy', response.json())

    def test_get_statistics(self):
        user = User.objects.create(telegram_id=12345)

        statistics = Statistics.objects.create(user=user, total_steps=1000, total_distance=5.0, total_rewards=10)

        url = reverse('get_statistics', args=[user.telegram_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_steps', response.json())
        self.assertEqual(response.json()['total_steps'], statistics.total_steps)

    def test_walk_history(self):
        user = User.objects.create(telegram_id=12345)
        walk = Walk.objects.create(user=user, start_time=now())

        url = reverse('walk_history', args=[user.telegram_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.json())
        self.assertEqual(len(response.json()['results']), 1)


class WalkAPITestCase(APITestCase):
    def test_start_walk(self):
        user = User.objects.create(telegram_id=12345)
        url = reverse('start_walk')
        data = {'telegram_id': user.telegram_id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('walk_id', response.json())

    def test_update_walk(self):
        user = User.objects.create(telegram_id=12345)
        walk = Walk.objects.create(user=user, start_time=now())
        url = reverse('update_walk')
        data = {'walk_id': walk.id, 'steps': 100, 'avg_speed': 5, 'telegram_id': user.telegram_id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['walk_steps'], 100)

    def test_finish_walk(self):
        user = User.objects.create(telegram_id=12345)
        walk = Walk.objects.create(user=user, start_time=now())
        url = reverse('finish_walk')
        data = {'walk_id': walk.id, 'telegram_id': user.telegram_id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_reward', response.json())

    def test_stop_walk(self):
        user = User.objects.create(telegram_id=12345)
        walk = Walk.objects.create(user=user, start_time=now())
        url = reverse('stop_walk')
        data = {'walk_id': walk.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tasks_complete(self):
        user = User.objects.create(telegram_id=12345)
        task = Task.objects.create(user=user, name="Complete walk", reward=5)

        self.assertFalse(task.is_completed)

        url = reverse('tasks_complete')
        data = {
            'task_id': task.id,
            'telegram_id': user.telegram_id
        }
        response = self.client.post(url, data, format='json')

        print("Response status:", response.status_code)
        print("Response data:", response.json())

        task.refresh_from_db()
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(task.is_completed)
        self.assertEqual(user.points, 5)


