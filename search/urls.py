# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url
from search.views import search

urlpatterns = patterns(
    '',
    url(r'^$', search, name='search_index'),
)
