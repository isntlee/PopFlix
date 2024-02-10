from django.contrib import admin
from .models import Content, Channel, Group


class ContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'rating', 'channel']


class ChannelAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'superchannel', 'id']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'id']


admin.site.register(Content, ContentAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Group, GroupAdmin)
