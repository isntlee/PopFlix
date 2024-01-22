from rest_framework import generics
from contents.models import Channel, Content
from .serializers import ChannelSerializer, ContentSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


# Note: This will have to be refactored, 'thin views, fat models', remember
# And error handling, input validation

class ListView(generics.ListAPIView):
    serializer_class = ChannelSerializer

    def get_slugs(self):
        path = self.kwargs['path']
        slugs = path.split('/')
        return [slug.lower() for slug in reversed(slugs) if slug]


    def dispatch(self, request, *args, **kwargs):
        self.slugs = self.get_slugs()

        try:
            channel_obj = Channel.objects.get(slug=self.slugs[0])
            if isinstance(channel_obj, Channel):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("Object is not a Channel.")
        except ObjectDoesNotExist:
            try:
                content_obj = Content.objects.get(slug=self.slugs[0])
                if isinstance(content_obj, Content):
                    print('\n\n ### Testing#13', self.kwargs['path'], '\n')
                    detail_view = DetailView.as_view()
                    request._content_obj = content_obj
                    return detail_view(request, *args, **kwargs)
                else:
                    raise Http404("Object is not a Content.")
            except ObjectDoesNotExist:
                raise Http404("No Channel or Content matches the given query.")

        
    def get_queryset(self):  
        self.slugs = self.get_slugs()
        pk = Channel.objects.get(slug=self.slugs[0]).pk

        if pk is None:
            return Channel.objects.filter(active=True)[:20]
        else:
            return Channel.objects.filter(id=pk)
        

class DetailView(generics.ListAPIView):
   serializer_class = ContentSerializer

   def get_queryset(self): 
        content_obj = self.request._content_obj 
        pk = content_obj.pk

        if pk is None:
            return Content.objects.filter(active=True)[:20]
        else:
            return Content.objects.filter(id=pk)
        
