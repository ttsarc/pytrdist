# -*- encoding: utf-8 -*-
try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from search.views import search

urlpatterns = patterns('',
                url(r'^$', search, name='search_index'),
            )
