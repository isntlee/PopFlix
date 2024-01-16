from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from django.utils.text import slugify



class Channel(models.Model):    
    title = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    active = models.BooleanField(default=True, null=True)
    picture_url = models.URLField(max_length=250, null=True, blank=True)
    parent = models.ForeignKey("self", related_name='children', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):  
        return self.title
    

    def get_channel_ratings():
        results = {}

        for channel in Channel.objects.all():
            child_channels, subchannel_total = channel.get_all_subchannels()  
            grouped_by_index = zip(*subchannel_total)
            subchannel_summed = [sum(group) for group in grouped_by_index]

            try:
                channel_avg = subchannel_summed[0] / subchannel_summed[1]
            except IndexError:
                channel_avg = 0

            results[channel.title] = round(channel_avg, 3)

        return results


    def get_all_subchannels(self, include_self=True):
        answer_list = []
        subchannel_total = []
        stack = []

        if include_self:
            stack.append(self)

        while stack:
            node = stack.pop()    
            answer_list.append(node)

            if isinstance(node, Channel) and node.contents.exists():
                if node.contents.exists():
                    contents_ratings = node.contents.values_list('rating', flat=True) 
                    channel_ratings = [float(sum(contents_ratings)), len(contents_ratings)]
                    subchannel_total.append(channel_ratings)

            for subchannel in Channel.objects.filter(parent=node):
                if subchannel.contents.exists():
                    contents_ratings = subchannel.contents.values_list('rating', flat=True) 
                    subchannel_ratings = [float(sum(contents_ratings)), len(contents_ratings)]
                    subchannel_total.append(subchannel_ratings)

                stack.append(subchannel)    

        return answer_list, subchannel_total
    


class Content(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=2500)
    genre = models.CharField(max_length=250)
    authors = models.CharField(max_length=250)
    file_url = models.URLField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    rating = models.DecimalField(default=1, max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    channel = models.ForeignKey(Channel, related_name='contents', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)   
        super().save(*args, **kwargs)
    
    
 