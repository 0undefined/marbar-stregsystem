from django.apps import AppConfig

class CmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cms'

    def ready(self):
        from .models import MarbarConsumer
        from stregsystem.settings import DEFAULT_CONSUMERS

        for consumer in DEFAULT_CONSUMERS:
            MarbarConsumer.objects.get_or_create(name=consumer)
