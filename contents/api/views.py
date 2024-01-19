from rest_framework import generics
from contents.models import Channel, Content
from .serializers import ChannelSerializer, ContentSerializer
from django.shortcuts import get_object_or_404


class ChannelListView(generics.ListAPIView):
   serializer_class = ChannelSerializer

   def get_queryset(self):
      slug = self.kwargs.get('slug', None)
      if slug is None:
          return Channel.objects.filter(active=True)[:20]
      else: 
          channel_obj = get_object_or_404(Channel, slug=slug)
          return Channel.objects.select_related('parent').filter(parent_id=channel_obj.id)


class ContentListView(generics.ListAPIView):
   serializer_class = ContentSerializer

   def get_queryset(self):
      pk = self.kwargs.get('pk', None)
      if pk is None:
          return Content.objects.filter(active=True)[:20]
      else:
          return Content.objects.filter(channel_id=pk)
