from rest_framework import serializers
from contents.models import Channel, Content


class ContentSerializer(serializers.ModelSerializer):
   
   class Meta:
       model = Content
       fields = ['name','id', 'slug', 'rating', 'channel']
     

class ChannelSerializer(serializers.ModelSerializer):
    subchannel = serializers.SerializerMethodField()
    contents = ContentSerializer('contents', many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ['title', 'id', 'language', 'slug', 'active', 'superchannel', 'picture_url', 'subchannel', 'contents']

    def get_subchannel(self, obj):
        return [{'id': child.id, 'title': child.title, 'picture_url': child.picture_url} for child in obj.subchannel.all()]
