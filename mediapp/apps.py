from django.apps import AppConfig

class MediappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mediapp'

    def ready(self):
        from .ml_models.predict import predict