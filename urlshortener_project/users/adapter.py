# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        google_email = sociallogin.account.extra_data.get('email')
        emailEnding = google_email.split("@")[1]
        if 'alvaradoisd' not in emailEnding:
            raise ImmediateHttpResponse(HttpResponse('Please sign in with your Alvarado ISD email account.'))
