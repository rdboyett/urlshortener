from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from urlshortener_project.users.models import User
from ..models import ShortenedLink

class ShortenerModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='temporary', email='temporary@gmail.com', password='top_secret')
        self.shortLink = ShortenedLink.objects.create(user=self.user, short="lion", longURL="http://www.whatever.com")

    def test_shortenedLink_creation(self):
        self.assertTrue(isinstance(self.shortLink, ShortenedLink))
        self.assertEqual(self.shortLink.__str__(), self.shortLink.short)
        self.shortLink.longURL = "whatever error"
        self.assertRaises(ValidationError)


    def test_get_absolute_url(self):
        self.assertEqual(self.shortLink.get_absolute_url(), reverse('shortener:detail', kwargs={'pk': self.shortLink.pk}))

    def test_myURLs(self):
        shortList = ShortenedLink.objects.myURLs(self.user)
        for short in shortList:
            self.assertTrue(isinstance(short, ShortenedLink))
            self.assertEqual(short.user, self.user)

    def test_clean(self):
        invalidPossibleShorts = ['no space', '#', '~','!','@','$','%','^','&','*','(',')','+','=','{','}','[',']']
        for short in invalidPossibleShorts:
            self.shortLink.short = short
            self.assertRaises(ValidationError, self.shortLink.clean)

        validPossibleShorts = ['good','_', '1234234', '-']
        for short in validPossibleShorts:
            self.shortLink.short = short
            self.shortLink.clean()
            self.assertEqual(self.shortLink.short, short)

    def test_validate_unique_notAllowedList(self):
        notAllowedList = ['shortener','users','accounts','admin','api-auth']
        for item in notAllowedList:
            self.shortLink.short = item
            self.assertRaises(ValidationError, self.shortLink.validate_unique)

    def test_validate_unique_uniqueness(self):
        self.shortLinkSameName = ShortenedLink.objects.create(user=self.user, short="lion", longURL="http://www.whatever.com")
        self.assertRaises(ValidationError, self.shortLinkSameName.validate_unique)

    def test_update_hitNumber(self):
        nextHitNumber = self.shortLink.hitNumber + 1
        self.shortLink.update_hitNumber()
        self.assertEqual(self.shortLink.hitNumber, nextHitNumber)


