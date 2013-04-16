# -*- encoding: utf-8 -*-
try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from contact.views import general
urlpatterns = patterns('',
                       url(r'^$', general, name='contact'),
)
