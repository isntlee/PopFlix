from django.core.management.base import BaseCommand
import csv
from contents.models import Channel


class Command(BaseCommand):
    """
    A management command that calculates the average rating for each active Channel and its subchannels.
    It uses depth-first traversal to aggregate subchannel ratings and then calculates averages

    Methods:
    - `handle` executes the command, calling `get_channel_ratings` and writing the results to a csv file.
    - `get_channel_ratings` processes each active Channel, computes average ratings including subchannels.
    - `get_all_subchannels` performs an iterative depth-first traversal of a Channel hierarchy, 
       collecting and returning all visited Channels and their aggregate ratings, while optionally 
       including the starting Channel itself.
    """

    def handle(self, *args, **kwargs):
        results = self.get_channel_ratings()   
        sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        with open('results_channel_ratings.csv', 'w') as f:
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


    def get_all_subchannels(self, channel):
        answer_list = []
        subchannel_total = []
        stack = [channel]

        while stack:
            node = stack.pop()    
            answer_list.append(node)
            if isinstance(node, Channel) and node.contents.exists():
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
