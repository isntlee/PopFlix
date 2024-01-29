from django.test import TestCase
from contents.models import Group, Channel, Content
from django.core.exceptions import ValidationError



class GroupTestCase(TestCase):
    def setUp(self):
        self = Group.objects.create(title="Test Group")

    def test_group_creation(self):
        group = Group.objects.get(title="Test Group")
        self.assertEqual(group.title, "Test Group")

    def test_group_save(self):
        group = Group.objects.create(title="Test Group 2")
        self.assertEqual(group.slug, "test-group-2")

    def test_group_slug_generation(self):
        group = Group.objects.create(title="Test Group 3")
        self.assertEqual(group.slug, "test-group-3")

    def tearDown(self):
        Group.objects.all().delete()



class ChannelTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(title="Test Group")
        self.channel = Channel.objects.create(title="Test Channel", language="English")
        self.content = Content.objects.create(name="Test Content", genre="Genre", authors="Author", file_url="http://example.com", channel=self.channel)

    def test_channel_creation(self):
        channel = Channel.objects.get(title="Test Channel")
        self.assertEqual(channel.title, "Test Channel")
        self.assertEqual(channel.language, "English")

    def test_channel_save(self):
        channel = Channel.objects.create(title="Test Channel 2", language="English")
        self.assertEqual(channel.slug, "test-channel-2")

    def test_relationship_between_models(self):
        self.channel.groups.add(self.group)
        self.assertEqual(list(self.channel.groups.all()), [self.group])

    def test_channel_clean(self):
        superchannel = Channel.objects.get(title="Test Channel")
        channel = Channel.objects.create(title="Test Channel 3", language="English", superchannel=superchannel)
        Content.objects.create(name="Test Content 2", genre="Genre", authors="Author", file_url="http://example.com", channel=channel)

        with self.assertRaises(ValidationError):
            channel.clean()

        channel.superchannel.contents.clear()
        channel.clean() 

    def test_get_all_superchannels(self):
        superchannel = Channel.objects.create(title="Super Channel", language="English")
        channel = Channel.objects.create(title="Channel", language="English", superchannel=superchannel)
        self.assertEqual(channel.get_all_superchannels(include_self=False), ["super channel"])

    def test_add_group_to_superchannels(self):
        group = Group.objects.create(title="Test Group 2")
        channel = Channel.objects.create(title="Test Channel 4", language="English")

        self.channel.groups.add(group)
        self.channel.superchannel = channel

        self.channel.save()
        self.assertEqual(list(self.channel.groups.all()), [group])

    def test_channel_slug_generation(self):
        channel = Channel.objects.create(title="Test Channel 4", language="English")
        self.assertEqual(channel.slug, "test-channel-4")

    def tearDown(self):
        Channel.objects.all().delete()
        Content.objects.all().delete()
        Group.objects.all().delete()



class ContentTestCase(TestCase):
    def setUp(self):
        Content.objects.create(name="Test Content", genre="Genre", authors="Author", file_url="http://example.com")

    def test_content_creation(self):
        content = Content.objects.get(name="Test Content")
        self.assertEqual(content.name, "Test Content")
        self.assertEqual(content.genre, "Genre")
        self.assertEqual(content.authors, "Author")
        self.assertEqual(content.file_url, "http://example.com")

    def test_content_save(self):
        content = Content.objects.create(name="Test Content 2", genre="Genre", authors="Author", file_url="http://example.com")
        self.assertEqual(content.slug, "test-content-2")

    def test_content_slug_generation(self):
        content = Content.objects.create(name="Test Content 3", genre="Genre", authors="Author", file_url="http://example.com")
        self.assertEqual(content.slug, "test-content-3")

    def test_get_channel(self):
        content = Content.objects.get(name="Test Content")
        self.assertEqual(content.get_channel(), content.channel)

    def tearDown(self):
        Content.objects.all().delete()