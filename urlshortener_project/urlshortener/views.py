# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView, DeleteView

from braces.views import LoginRequiredMixin
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import ShortenedLink
from .forms import ShortendedLinkForm, UpdateShortenedLinkForm
from .serializers import ShortenedLinkSerializer, CreateShortenedLinkSerializer
from .permissions import IsOwnerOrReadOnly

class DefaultFormMixin(object):

    def get_context_data(self, **kwargs):
        context = super(DefaultFormMixin, self).get_context_data(**kwargs)
        context['shortForm'] = ShortendedLinkForm
        return context



class UrlListView(LoginRequiredMixin, DefaultFormMixin, ListView):
    context_object_name = 'myURLs_list'

    def get_queryset(self):
        return ShortenedLink.objects.myURLs(self.request.user)


class UrlDetailView(LoginRequiredMixin, DefaultFormMixin, DetailView):
    model = ShortenedLink
    context_object_name = 'myShortenedLink'


class UrlCreateView(LoginRequiredMixin, CreateView):
    form_class = ShortendedLinkForm
    template_name = 'pages/home.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.short = form.generateCode()
        self.object.save()
        return super(UrlCreateView, self).form_valid(form)


class UrlUpdateView(LoginRequiredMixin, DefaultFormMixin, UpdateView):
    model = ShortenedLink
    form_class = UpdateShortenedLinkForm


class UrlDeleteView(LoginRequiredMixin, DefaultFormMixin, DeleteView):
    model = ShortenedLink
    success_url = reverse_lazy('shortener:myURLs')


class UrlRedirectView(RedirectView):
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        shortenedLink = get_object_or_404(ShortenedLink, short=kwargs['short'])
        shortenedLink.update_hitNumber()
        self.url = shortenedLink.longURL
        return super(UrlRedirectView, self).get_redirect_url(*args, **kwargs)


class APIList(ListAPIView):
    queryset = ShortenedLink.objects.all()
    serializer_class = ShortenedLinkSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class APICreate(CreateAPIView):
    queryset = ShortenedLink.objects.all()
    serializer_class = CreateShortenedLinkSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        shortCode = serializer.generateCode()
        serializer.save(user=self.request.user, short=shortCode)


class APIDetail(RetrieveUpdateDestroyAPIView):
    queryset = ShortenedLink.objects.all()
    serializer_class = ShortenedLinkSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.validate()
        serializer.save(user=self.request.user)

