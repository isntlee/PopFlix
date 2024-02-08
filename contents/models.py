from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models, transaction

# Note: This will all have to be reviewed/studied
#       - comments to add, explain superchannel/subchannel


class Group(models.Model):
    title = models.CharField(max_length=250)
    active = models.BooleanField(default=True, null=True)
    picture_url = models.URLField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)

    def __str__(self):  
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)   
        super().save(*args, **kwargs)



class ChannelManager(models.Manager):
    def get_active_channels(self):
        return self.filter(active=True)[:20]

    def get_channels_by_pk(self, pk):
        return self.filter(id=pk)

    def get_channels_by_group(self, group_name, queryset):
        try:
            group = Group.objects.get(slug=group_name)
            subchannels = queryset.first().subchannel.all()
            return subchannels.filter(groups__in=[group])
        
        except Group.DoesNotExist:
            return queryset.none()
        


class Channel(models.Model):    
    title = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    active = models.BooleanField(default=True, null=True)
    picture_url = models.URLField(max_length=250, null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    superchannel = models.ForeignKey("self", related_name='subchannel', on_delete=models.SET_NULL, null=True, blank=True)
    objects = ChannelManager()
    
    def __str__(self):  
        return self.title

    def clean(self):
        if self.superchannel and self.superchannel.contents.exists():
            raise ValidationError("Can't add a subchannel to a channel with existing contents")
        elif not self.superchannel:
            raise ValidationError("Can't create a channel without either contents or subchannels") 
        super().clean()
  

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)   
        super().save(*args, **kwargs)
        if self.superchannel:
            transaction.on_commit(self.add_group_to_superchannels)


    def get_all_superchannels(self, include_self=True):
        superchannel_list = [] 
        if include_self:
            superchannel_list.append(self.title.lower())
        current_channel = self.superchannel

        while current_channel is not None:
            superchannel_list.append(current_channel.title.lower())
            current_channel = current_channel.superchannel

        return superchannel_list
    

    def add_group_to_superchannels(self):
        if not self.groups.exists():
            return False

        superchannel_list = self.get_all_superchannels(include_self=False)
        channel_objs = Channel.objects.prefetch_related('groups').filter(slug__in=superchannel_list)

        for channel_obj in channel_objs:
            channel_obj.groups.add(*self.groups.all())



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
