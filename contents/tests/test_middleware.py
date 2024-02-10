from django.test import RequestFactory, TestCase
from django.http import HttpResponse
from core.middleware import IgnoreFaviconMiddleware

class IgnoreFaviconMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = IgnoreFaviconMiddleware(lambda req: HttpResponse())

    def test_ignore_favicon(self):
        request = self.factory.get('/favicon.ico')
        response = self.middleware.__call__(request)
        self.assertEqual(response.status_code,  204)

    def test_non_favicon(self):
        request = self.factory.get('/some/other/path')
        response = self.middleware.__call__(request)
        self.assertNotEqual(response.status_code,  204)
        self.assertEqual(response.status_code,  200)
