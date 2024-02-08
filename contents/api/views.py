from django.http import Http404
from rest_framework import generics
from contents.models import Channel, Content
from .serializers import ChannelSerializer, ContentSerializer
from .validators import UrlValidator

#Note: This will all have to be reviewed/studied


class ListView(generics.ListAPIView):
    serializer_class = ChannelSerializer
    paginate_by =  20


    def dispatch(self, request, *args, **kwargs): 
        slugs = self.get_slugs()
        obj = UrlValidator.check_url(slugs)
        self.group = request.GET.get('group', None)

        if isinstance(obj, Channel):
            return super().dispatch(request, *args, **kwargs)  
        elif isinstance(obj, Content):  
            detail_view = DetailView.as_view()
            request._slug_obj = obj.slug
            return detail_view(request, *args, **kwargs)
        else:
            raise Http404("No Channel or Content matches the given url")
     

    def get_queryset(self):  
        slugs = self.get_slugs()
        pk = Channel.objects.get(slug=slugs[0]).pk
        group = self.request.query_params.get('group', None)

        if pk is None:
            queryset = Channel.objects.get_active_channels()
        else:
            queryset = Channel.objects.get_channels_by_pk(pk)

        if group is not None:
            queryset = Channel.objects.get_channels_by_group(group, queryset)
        return queryset


    def get_slugs(self):
        path = self.kwargs.get('path') 
        if not path:
            raise ValueError("URL path cannot be empty, please try again")
        
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
        
        
