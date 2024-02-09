from django.core.exceptions import ValidationError
from contents.models import Channel, Content


class UrlValidator:
    @staticmethod
    def check_url(slugs):
        print('\n\n##Testing#1', slugs, '\n')
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
                raise ValidationError("Sorry we can't find that page, please check the url")

    @staticmethod
    def check_super_channels(obj, slugs):
        super_channels = obj.get_all_superchannels()
        if slugs != super_channels:
            raise ValidationError("Sorry we can't find that page, please check the url")
