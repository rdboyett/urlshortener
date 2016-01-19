from django.test import TestCase
from django.core.urlresolvers import reverse

from urlshortener_project.users.models import User
from ..models import ShortenedLink

class ShortenerViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='temporary', email='temporary@gmail.com', password='top_secret')
        self.client.login(username='temporary', password='top_secret')
        self.shortLink = ShortenedLink.objects.create(user=self.user, short="lion", longURL="http://www.whatever.com")

    def test_UrlListView(self):
        url = reverse("shortener:myURLs")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.shortLink.short, resp.content)

    def test_UrlCreateView(self):
        url = reverse("shortener:createURL")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(url, {'longURL': 'http://www.whatever.com'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('http://www.whatever.com', resp.content)

    def test_UrlUpdateView(self):
        url = reverse("shortener:updateURL", kwargs={'pk': self.shortLink.pk})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.shortLink.short, resp.content)

    def test_UrlRedirectView(self):
        url = reverse("redirectURL", kwargs={'short': self.shortLink.short})
        resp = self.client.get(url, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, self.shortLink.longURL)
