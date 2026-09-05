from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from contents.models import Channel, Content, Group


class ListViewTestCase(TestCase):
    def setUp(self):
        Channel.objects.create(title="Channel1", )
        Content.objects.create(name="Content1")
        Group.objects.create(title='Group1')

    def test_get_request(self):
        path = Channel.objects.first().slug
        response = self.client.get(reverse('list_view', kwargs={'path': path, 'group': ''}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_channel(self):
        response = self.client.get(reverse('list_view', kwargs={'path': 'invalid_channel', 'group': ''}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_group(self):
        response = self.client.get(reverse('list_view', kwargs={'path': '', 'group': 'invalid_group'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        Channel.objects.all().delete()
        Group.objects.all().delete()
        Content.objects.all().delete()


class DetailViewTestCase(TestCase):
    def setUp(self):
        channel = Channel.objects.create(title="Channel1")
        Content.objects.create(name="Content1", channel=channel)

    def test_get_request(self): 
        client = Client()
        path = Channel.objects.first().slug + '/' + Content.objects.first().slug
        response = client.get(reverse('list_view', kwargs={'path': path, 'group': ''}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_content(self):
        channel = Channel.objects.create(title="Channel2")
        response = self.client.get(reverse('list_view', kwargs={'path': channel.slug + '/invalid_content', 'group': ''}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        Channel.objects.all().delete()
        Content.objects.all().delete()


class ActiveFlagTestCase(TestCase):
    def test_inactive_channel(self):
        channel = Channel.objects.create(title="Hidden", active=False)
        Content.objects.create(name="Buried", channel=channel)
        response = self.client.get(reverse('list_view', kwargs={'path': channel.slug, 'group': ''}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_active_channel(self):
        channel = Channel.objects.create(title="Shown", active=True)
        response = self.client.get(reverse('list_view', kwargs={'path': channel.slug, 'group': ''}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inactive_content(self):
        channel = Channel.objects.create(title="Open", active=True)
        content = Content.objects.create(name="Secret", channel=channel, active=False)
        path = channel.slug + '/' + content.slug
        response = self.client.get(reverse('list_view', kwargs={'path': path, 'group': ''}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_active_content(self):
        channel = Channel.objects.create(title="Public", active=True)
        content = Content.objects.create(name="Visible", channel=channel, active=True)
        path = channel.slug + '/' + content.slug
        response = self.client.get(reverse('list_view', kwargs={'path': path, 'group': ''}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        Channel.objects.all().delete()
        Content.objects.all().delete()
