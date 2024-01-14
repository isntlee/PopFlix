from django.core.management.base import BaseCommand
from contents.models import Channel


class Command(BaseCommand):
    help = 'Runs the websocket script'

    def handle(self, *args, **kwargs):
        Channel.get_all_ratings()
