from django.core.management.base import BaseCommand
from contents.models import Channel, Content


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        content_obj = Content.objects.filter(slug='empire').first()    
        channel = Content.get_channel(content_obj)
        parents = Channel.get_all_parents(channel)

        print('\n\n## parents_list:', parents, '\n\n')
