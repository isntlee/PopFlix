from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Note: should change the name of parent/children to something more domain correct 

class Channel(models.Model):    
    title = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    active = models.BooleanField(default=True, null=True)
    picture_url = models.URLField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    parent = models.ForeignKey("self", related_name='children', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):  
        return self.title

    # Note: work out a solution for adding channels in future, probably request.user.is_superuser. 

    def clean(self):
        if self.parent and self.parent.contents.exists():
            raise ValidationError("Can't add a subchannel to a channel with existing contents")
        elif not self.parent:
            raise ValidationError("Can't create a channel without either contents or subchannels") 
        super().clean()
  
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)   
        super().save(*args, **kwargs)


    def get_channel_ratings():
        results = {}

        for channel in Channel.objects.all(active=True):
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
    

    def get_all_parents(self, include_self=True):
        parent_list = []
        
        if include_self:
            parent_list.append(self.title.lower())

        current_channel = self.parent
        while current_channel is not None:
            parent_list.append(current_channel.title.lower())
            current_channel = current_channel.parent

        return parent_list
    


class Content(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=2500)
    genre = models.CharField(max_length=250)
    authors = models.CharField(max_length=250)
    file_url = models.URLField(max_length=250)
    active = models.BooleanField(default=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    rating = models.DecimalField(default=1, max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    channel = models.ForeignKey(Channel, related_name='contents', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name 
    
    def get_channel(self):
        return self.channel
    
    def clean(self):
       if self.channel.children.exists():
           raise ValidationError("Can't add contents to a channel with existing subchannels")
       super().clean()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)   
        super().save(*args, **kwargs)
