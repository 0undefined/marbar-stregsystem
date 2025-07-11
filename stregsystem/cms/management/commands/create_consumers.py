from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Create default consumers"

    def handle(self, *args, **kwargs):
        try:
            from cms.models import MarbarConsumer
            from stregsystem.settings import DEFAULT_CONSUMERS

            for consumer in DEFAULT_CONSUMERS:
                MarbarConsumer.objects.get_or_create(name=consumer)
        except:
            raise CommandError("Failed to create consumers")
