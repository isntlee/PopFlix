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
