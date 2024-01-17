from rest_framework import generics
from contents.models import Channel, Content
from .serializers import ChannelSerializer, ContentSerializer


class ChannelListView(generics.ListAPIView):
   queryset = Channel.objects.all()
   serializer_class = ChannelSerializer


class ChannelDetailView(generics.RetrieveAPIView):
   queryset = Channel.objects.all()
   serializer_class = ChannelSerializer


class ContentListView(generics.ListAPIView):
   queryset = Content.objects.all()
   serializer_class = ContentSerializer


class ContentDetailView(generics.RetrieveAPIView):
   queryset = Content.objects.all()
   serializer_class = ContentSerializer


# To add both content serializers 