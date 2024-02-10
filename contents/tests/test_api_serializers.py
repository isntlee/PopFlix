from unittest import TestCase
from contents.models import Group, Content, Channel
from contents.api.serializers import GroupSerializer, ContentSerializer, ChannelSerializer


class GroupSerializerTest(TestCase):
    def setUp(self):
        self.group_attributes = {
            'title': 'Test Group',
            'id': 1,
            'slug': 'test-group'
        }

        self.group = Group.objects.create(**self.group_attributes)
        self.serializer = GroupSerializer(instance=self.group)

    def tearDown(self):
        self.group.delete()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['title', 'id', 'slug']))

    def test_group_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.group_attributes['title'])
        self.assertEqual(data['id'], self.group_attributes['id'])
        self.assertEqual(data['slug'], self.group_attributes['slug'])


class ContentSerializerTest(TestCase):
    def setUp(self):
        self.content_attributes = {
            'name': 'Test Content',
            'rating': '4.0',
            'slug': 'test-content'
        }

        self.content = Content.objects.create(**self.content_attributes)
        self.serializer = ContentSerializer(instance=self.content)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['name', 'id', 'slug', 'rating', 'channel']))

    def test_content_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.content_attributes['name'])
        self.assertEqual(data['rating'], self.content_attributes['rating'])
        self.assertEqual(data['slug'], self.content_attributes['slug'])

    def tearDown(self):
        Content.objects.all().delete()


class ChannelSerializerTest(TestCase):
    def setUp(self):
        self.channel_attributes = {
            'title': 'Test Channel',
            'slug': 'test-channel',
            'language': 'English',
            'active': True,
            'picture_url': 'http://example.com/image.jpg',
        }

        self.channel = Channel.objects.create(**self.channel_attributes)
        self.serializer = ChannelSerializer(instance=self.channel)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['title', 'id', 'language', 'slug', 'active', 'superchannel', 'picture_url', 'subchannel', 'contents', 'groups']))

    def test_channel_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.channel_attributes['title'])
        self.assertEqual(data['slug'], self.channel_attributes['slug'])
        self.assertEqual(data['language'], self.channel_attributes['language'])
        self.assertEqual(data['active'], self.channel_attributes['active'])
        self.assertEqual(data['picture_url'], self.channel_attributes['picture_url'])

    def test_get_subchannel(self):
        result = self.serializer.get_subchannel(self.channel)
        self.assertEqual(result, [])

    def tearDown(self):
        Channel.objects.all().delete()
