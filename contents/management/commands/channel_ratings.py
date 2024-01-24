from django.core.management.base import BaseCommand
from contents.models import Channel
import csv


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        results = self.get_channel_ratings()   
        sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        with open('results.csv', 'w') as f:
            fieldnames = ['Channel Title', 'Average Rating']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for key, value in sorted_results.items():
                writer.writerow({'Channel Title': key, 'Average Rating': value})


    def get_channel_ratings(self):
        results = {}
        for channel in Channel.objects.filter(active=True):
            child_channels, subchannel_total = self.get_all_subchannels(channel)  
            grouped_by_index = zip(*subchannel_total)
            subchannel_summed = [sum(group) for group in grouped_by_index]

            try:
                channel_avg = subchannel_summed[0] / subchannel_summed[1]
            except IndexError:
                channel_avg = 0

            results[channel.title] = round(channel_avg, 3)

        return results


    def get_all_subchannels(self, channnel, include_self=True):
        answer_list = []
        subchannel_total = []
        stack = []

        if include_self:
            stack.append(channnel)

        while stack:
            node = stack.pop()    
            answer_list.append(node)
            if isinstance(node, Channel) and node.contents.exists():
                if node.contents.exists():
                    contents_ratings = node.contents.values_list('rating', flat=True) 
                    channel_ratings = [float(sum(contents_ratings)), len(contents_ratings)]
                    subchannel_total.append(channel_ratings)

            for subchannel in Channel.objects.filter(superchannel=node):
                if subchannel.contents.exists():
                    contents_ratings = subchannel.contents.values_list('rating', flat=True) 
                    subchannel_ratings = [float(sum(contents_ratings)), len(contents_ratings)]
                    subchannel_total.append(subchannel_ratings)

                stack.append(subchannel)    

        return answer_list, subchannel_total

        
