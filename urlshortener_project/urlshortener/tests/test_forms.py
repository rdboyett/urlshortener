from django.test import TestCase
from django.core.urlresolvers import reverse

from urlshortener_project.users.models import User
from ..models import ShortenedLink
from ..forms import ShortendedLinkForm, UpdateShortenedLinkForm

class ShortenerFormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='temporary', email='temporary@gmail.com', password='top_secret')
        self.client.login(username='temporary', password='top_secret')
        self.shortLink = ShortenedLink.objects.create(user=self.user, short="lion", longURL="http://www.whatever.com")

    def test_ShortendedLinkForm_valid(self):
        data = {'longURL': 'http://www.whatever.com'}
        form = ShortendedLinkForm(data=data)
        self.assertTrue(form.is_valid())

    def test_ShortendedLinkForm_invalid(self):
        possibleURLs = ['lksadjf', '']
        for url in possibleURLs:
            data = {'longURL': url}
            form = ShortendedLinkForm(data=data)
            self.assertFalse(form.is_valid())
