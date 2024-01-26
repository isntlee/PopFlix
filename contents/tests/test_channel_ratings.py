from django.test import TestCase
from contents.models import Channel, Content
from django.core.management import call_command
from contents.management.commands.channel_ratings import Command
import csv


class CommandTestCase(TestCase):
    def setUp(self):
        self.channel1 = Channel.objects.create(title='channel_1', active=True)
        self.channel2 = Channel.objects.create(title='channel_2', active=True)
        self.content1 = Content.objects.create(channel=self.channel1, name='content_1', rating=5)
        self.content2 = Content.objects.create(channel=self.channel1, name='content_2', rating=3)
        self.content3 = Content.objects.create(channel=self.channel2, name='content_3', rating=4)
        self.content4 = Content.objects.create(channel=self.channel2, name='content_4', rating=2)

    def tearDown(self):
        Channel.objects.all().delete()
        Content.objects.all().delete()

    def test_get_channel_ratings(self):
        command = Command()
        results = command.get_channel_ratings()
        self.assertEqual(results['channel_1'], 4.0)
        self.assertEqual(results['channel_2'], 3.0)
  
    def test_get_channel_ratings_no_contents(self):
        self.channel3 = Channel.objects.create(title='channel_3', active=True)

        command = Command()
        results = command.get_channel_ratings()
        self.assertEqual(results['channel_3'], 0.0)

    def test_get_all_subchannels(self):
        command = Command()
        channels, _ = command.get_all_subchannels(self.channel1)
        self.assertEqual(len(channels), 1)
   
    def test_get_all_subchannels_with_subchannels(self):
        self.subchannel = Channel.objects.create(title='subchannel_1', superchannel=self.channel1)

        command = Command()
        channels, _ = command.get_all_subchannels(self.channel1)
        self.assertEqual(len(channels), 2)

    def test_command(self):
        call_command('channel_ratings')

        with open('results.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            rows = [row for row in reader if row]

        expected_rows = [['channel_1', '4.0'], ['channel_2', '3.0']]
        self.assertEqual(rows, expected_rows)