from rest_framework import generics
from contents.models import Channel, Content
from .serializers import ChannelSerializer, ContentSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

# Note: This will have to be refactored, 'thin views, fat models', remember
# And error handling, input validation, get_object_or_404 everywhere 

class ListView(generics.ListAPIView):
    serializer_class = ChannelSerializer

    def dispatch(self, request, *args, **kwargs):
        slugs = self.get_slugs()
        obj = self.check_url(slugs)

        if isinstance(obj, Channel):
            return super().dispatch(request, *args, **kwargs)  
        elif isinstance(obj, Content):  
            detail_view = DetailView.as_view()
            request._slug_obj = obj.slug
            return detail_view(request, *args, **kwargs)
        else:
            raise Http404("No Channel or Content matches the given query.")
     
    def get_queryset(self):  
        slugs = self.get_slugs()
        pk = Channel.objects.get(slug=slugs[0]).pk

        if pk is None:
            return Channel.objects.filter(active=True)[:20]
        else:
            return Channel.objects.filter(id=pk)
        
    def check_url(self, slugs):
        slug = slugs[0]
        try:
            obj = Channel.objects.get(slug=slug)
            self.check_super_channels(obj, slugs)
            return obj
        except Channel.DoesNotExist:

            try:
                obj = Content.objects.get(slug=slug)
                parent = obj.channel
                content_slugs = slugs[1:]
                self.check_super_channels(parent, content_slugs)
                return obj
            except Content.DoesNotExist:
                raise Http404("Sorry we cannot find that page, please check the url")

    def check_super_channels(self, obj, slugs):
        super_channels = obj.get_all_superchannels()
        if slugs != super_channels:
            raise Http404("Sorry we cannot find that page, please check the url")

    def get_slugs(self):
        path = self.kwargs['path']
        slugs = path.split('/')
        return [slug.lower() for slug in reversed(slugs) if slug]
        


class DetailView(generics.RetrieveAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self): 
        return Content.objects.filter(active=True)

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            return self.get_queryset()[0]
        else:
            return Content.objects.get(pk=pk)
        
