from django.core.management.base import BaseCommand
from contents.models import Channel


class Command(BaseCommand):
    help = 'Runs the websocket script'

    def handle(self, *args, **kwargs):
        results = Channel.get_channel_ratings()
        print('\n\n Results:', results)
