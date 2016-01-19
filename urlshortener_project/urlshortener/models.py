from __future__ import unicode_literals
import re

from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.models import (TimeStampedModel)
from django.core.exceptions import ValidationError

from urlshortener_project.users.models import User


class ShortenedLinkManager(models.Manager):

    use_for_related_fields = True

    def myURLs(self, user):
        return self.filter(user=user)


class ShortenedLink(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    short = models.CharField(unique=True, max_length=65, error_messages={'unique': 'This word is already used.'})
    longURL = models.URLField(max_length=200)
    hitNumber = models.IntegerField(default=0)

    def __str__(self):
        return self.short

    objects = ShortenedLinkManager()

    def get_absolute_url(self):
        return reverse('shortener:detail', kwargs={'pk': self.pk})

    def clean(self):
        #Check that short has no space and is Letters, Numbers, Dashes and Underscores only.
        if not re.match("^[A-Za-z0-9_-]*$", self.short):
            raise ValidationError({'short': ('Letters, Numbers, Dashes and Underscores only.')})

    def validate_unique(self, *args, **kwargs):
        super(ShortenedLink, self).validate_unique(*args, **kwargs)

        #Validate words that the app uses in urls.py
        notAllowedList = ['shortener','users','accounts','admin','api-auth']
        for item in notAllowedList:
            if self.short == item:
                raise ValidationError({'short':['This word is already used.',]})

        #Validate the uniqueness of self.short
        queryList = self.__class__.objects.filter(short=self.short)
        for query in queryList:
            if self.id:
                if query.id != self.id:
                    raise ValidationError({'short':['This word is already used.',]})

    def update_hitNumber(self):
        self.hitNumber += 1
        self.save()
