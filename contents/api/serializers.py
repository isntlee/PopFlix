from rest_framework import serializers
from contents.models import Channel, Content


class ContentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Content
       fields = ['name', 'slug', 'rating', 'channel']


class ChannelSerializer(serializers.ModelSerializer):
#    content = ContentSerializer(many=True, read_only=True)

   class Meta:
       model = Channel
       fields = ['title', 'language', 'slug', 'active', 'parent', 'content']