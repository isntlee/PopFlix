from django.http import Http404
from contents.models import Channel, Content


class UrlValidator:
    """
    A utility class for validating URLs against channel and content slugs.
    
    This class provides static methods to check the existence of channels and contents
    based on the slug and ensures that the URL matches the hierarchy of superchannels.
    """

    @staticmethod
    def check_url(slugs):     
        slug = slugs[0]
        try:
            obj = Channel.objects.get(slug=slug)
            UrlValidator.check_super_channels(obj, slugs)
            return obj
        except Channel.DoesNotExist:
            try:
                obj = Content.objects.get(slug=slug)
                parent = obj.channel
                content_slugs = slugs[1:]
                UrlValidator.check_super_channels(parent, content_slugs)
                return obj
            except Content.DoesNotExist:
                raise Http404("Sorry we can't find that page, please check the url")

    @staticmethod
    def check_super_channels(obj, slugs):
        super_channels = obj.get_all_superchannels()
        if slugs != super_channels:
            raise Http404("Sorry we can't find that page, please check the url")
