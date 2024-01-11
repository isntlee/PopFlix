from django.contrib import admin
from .models import Content, Channel


class ContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'rating']


class ChannelAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']


admin.site.register(Content, ContentAdmin)
admin.site.register(Channel, ChannelAdmin)