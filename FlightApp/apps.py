from django.apps import AppConfig


class FlightappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FlightApp'

    def ready(self):
        from . import signals

