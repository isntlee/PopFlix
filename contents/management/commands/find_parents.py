from django.core.management.base import BaseCommand
from contents.models import Channel, Content
import csv


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # This will have to be changed, slug='empire'

        content_obj = Content.objects.get(slug='empire')    
        channel = Content.get_channel(content_obj)
        parents = Channel.get_all_parents(channel)

        return parents