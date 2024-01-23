from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Note: should change the name of superchannel/subchannel to something more domain correct 

class Channel(models.Model):    
    title = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    active = models.BooleanField(default=True, null=True)
    picture_url = models.URLField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    superchannel = models.ForeignKey("self", related_name='subchannel', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):  
        return self.title

    # Note: work out a solution for adding channels in future, probably request.user.is_superuser. 

    def clean(self):
        if self.superchannel and self.superchannel.contents.exists():
            raise ValidationError("Can't add a subchannel to a channel with existing contents")
        elif not self.superchannel:
            raise ValidationError("Can't create a channel without either contents or subchannels") 
        super().clean()
  

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)   
        super().save(*args, **kwargs)


    def get_all_superchannels(self, include_self=True):
        superchannel_list = [] 

        if include_self:
            superchannel_list.append(self.title.lower())
        current_channel = self.superchannel

        while current_channel is not None:
            superchannel_list.append(current_channel.title.lower())
            current_channel = current_channel.superchannel

        return superchannel_list
    


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
       if self.channel.subchannel.exists():
           raise ValidationError("Can't add contents to a channel with existing subchannels")
       super().clean()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)   
        super().save(*args, **kwargs)
