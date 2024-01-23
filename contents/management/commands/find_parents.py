from django.core.management.base import BaseCommand
from contents.models import Channel, Content

# This is all going to be removed soon enough

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        content_obj = Content.objects.filter(slug='empire').first()    
        channel = Content.get_channel(content_obj)
        superchannels = Channel.get_all_superchannels(channel)

        print('\n\n## superchannel_list:', superchannels, '\n\n')
