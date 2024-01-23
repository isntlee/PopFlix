from django.contrib import admin
from .models import Content, Channel


class ContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'rating', 'channel']


class ChannelAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'superchannel', 'id']


admin.site.register(Content, ContentAdmin)
admin.site.register(Channel, ChannelAdmin)