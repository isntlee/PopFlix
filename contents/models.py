from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from django.utils.text import slugify



class Channel(models.Model):
        
    title = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    picture_url = models.URLField(max_length=250, null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def get_all_children(self, include_self=False):
      r = []
      if include_self:
          r.append(self)
      for c in Channel.objects.filter(parent=self):
          _r = c.get_all_children(include_self=True)
          if 0 < len(_r):
              r.extend(_r)
      return r
    
    def __str__(self):
        return self.title
    


class Content(models.Model):

    name = models.CharField(max_length=250)
    description = models.TextField(max_length=2500)
    genre = models.CharField(max_length=250)
    authors = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    rating = models.DecimalField(default=1, max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    file_url = models.URLField(max_length=250)
    channel = models.ForeignKey(Channel, related_name='contents', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    
