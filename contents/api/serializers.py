from rest_framework import serializers
from contents.models import Channel, Content, Group

### This will all have to be reviewed/studied

class GroupSerializer(serializers.ModelSerializer):  
   class Meta:
       model = Group
       fields = ['title', 'id', 'slug']


class ContentSerializer(serializers.ModelSerializer):  
   class Meta:
       model = Content
       fields = ['name', 'id', 'slug', 'rating', 'channel']
     

class ChannelSerializer(serializers.ModelSerializer):
    subchannel = serializers.SerializerMethodField()
    contents = ContentSerializer('contents', many=True, read_only=True)
    groups = GroupSerializer('groups', many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ['title', 'id', 'language', 'slug', 'active', 'superchannel', 'picture_url', 'subchannel', 'contents', 'groups']

    def get_subchannel(self, obj):
        return [{'id': child.id, 'title': child.title, 'picture_url': child.picture_url} for child in obj.subchannel.all()]
    
    def get_group(self, obj):
        return [{'id': group.id, 'title': group.title, 'slug': group.slug} for group in obj.groups.all()]
