from rest_framework import generics
from contents.models import Channel, Content
from .serializers import ChannelSerializer, ContentSerializer


class ChannelListView(generics.ListAPIView):
   serializer_class = ChannelSerializer

   def get_queryset(self):
      pk = self.kwargs.get('pk', None)
      if pk is None:
          return Channel.objects.all()
      else:
          return Channel.objects.filter(parent_id=pk)


class ContentListView(generics.ListAPIView):
   serializer_class = ContentSerializer

   def get_queryset(self):
      pk = self.kwargs.get('pk', None)
      if pk is None:
          return Content.objects.all()
      else:
          return Content.objects.filter(channel_id=pk)
