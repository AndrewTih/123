from django.apps import AppConfig


class MoveOnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'move_on'

    def ready(self):
        import move_on.signals