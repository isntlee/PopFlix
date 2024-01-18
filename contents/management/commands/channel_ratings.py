from django.core.management.base import BaseCommand
from contents.models import Channel
import csv


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        results = Channel.get_channel_ratings()   
        sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

        with open('results.csv', 'w') as f:
            fieldnames = ['Channel Title', 'Average Rating']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for key, value in sorted_results.items():
                writer.writerow({'Channel Title': key, 'Average Rating': value})
