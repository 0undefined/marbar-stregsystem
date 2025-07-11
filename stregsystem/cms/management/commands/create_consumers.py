from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = "Create default consumers"

    def handle(self, *args, **kwargs):
        try:
            from stregsystem.settings import DEFAULT_CONSUMERS

            # Create groups
            group_kitchens = Group.objects.get_or_create(name='kitchen')[0]
            group_users = Group.objects.get_or_create(name='user')[0]

            for consumer in DEFAULT_CONSUMERS:
                group_kitchens.user_set.add(
                    User.objects.get_or_create(username=consumer)[0]
                )


        except Exception as e:
            raise CommandError("Failed to create consumers: " + str(e))
