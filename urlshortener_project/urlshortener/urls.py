# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import UrlListView, UrlCreateView, UrlDetailView, UrlUpdateView, UrlDeleteView, APIList, APICreate, APIDetail

urlpatterns = [
    url(r'^$', UrlListView.as_view(), name="myURLs"),
    url(r'^(?P<pk>(\d+))/$', UrlDetailView.as_view(), name='detail'),
    url(r'^create/$', UrlCreateView.as_view(), name="createURL"), #ajax
    url(r'^update/(?P<pk>(\d+))/$', UrlUpdateView.as_view(), name="updateURL"),
    url(r'^delete/(?P<pk>(\d+))/$', UrlDeleteView.as_view(), name="deleteURL"),
    url(r'^api/list/$', APIList.as_view(), name="list_rest_api"),
    url(r'^api/create/$', APICreate.as_view(), name="create_rest_api"),
    url(r'^api/(?P<pk>(\d+))/$', APIDetail.as_view(), name="detail_rest_api"),
]
