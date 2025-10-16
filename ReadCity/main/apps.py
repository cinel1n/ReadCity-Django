import os

from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # # чтобы он выполнялся только при запуске сервера
        # if not os.environ.get('RUN_MAIN'):
        # import main.signals
        from. import signals  # noqa