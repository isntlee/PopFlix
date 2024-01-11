from django.db import models
from django.utils.text import slugify


class Content(models.Model):
        
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=2500)
    genre = models.CharField(max_length=250)
    authors = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    rating = models.PositiveIntegerField(default=0)
    file_url = models.URLField(max_length=250)

    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Channel(models.Model):
        
    title = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    picture_url = models.URLField(max_length=250)

    def __str__(self):
        return self.name
    
    
