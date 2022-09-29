from django.apps import AppConfig


class PlayGroundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'play_ground'

    def ready(self):
        from . import signals

