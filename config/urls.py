# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

from urlshortener_project.urlshortener.views import UrlCreateView, UrlRedirectView

#from urlshortener_project.urlshortener.views import

urlpatterns = [
    url(r'^$', UrlCreateView.as_view(), name="home"),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^shortener/', include("urlshortener_project.urlshortener.urls", namespace="shortener")),
    url(r'^users/', include("urlshortener_project.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Your stuff: custom urls includes go here
    url(r'^(?P<short>[-\w]+)/$', UrlRedirectView.as_view(), name='redirectURL'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permissin Denied")}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]
