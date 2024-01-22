from rest_framework import serializers
from contents.models import Channel, Content


class ContentSerializer(serializers.ModelSerializer):
   
   class Meta:
       model = Content
       fields = ['name','id', 'slug', 'rating', 'channel']
     


class ChannelSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    contents = ContentSerializer('contents', many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ['title', 'id', 'language', 'slug', 'active', 'parent', 'contents', 'children']

    def get_children(self, obj):
        return [{'id': child.id, 'title': child.title} for child in obj.children.all()]
