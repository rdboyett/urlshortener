from django.contrib import admin

from .models import ShortenedLink

class ShortenedLinkAdmin(admin.ModelAdmin):
    list_display = ('short', 'longURL', 'hitNumber')
    search_fields = ['short','longURL']

admin.site.register(ShortenedLink)
