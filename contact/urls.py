# -*- encoding: utf-8 -*-
try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from contact import contact
urlpatterns = patterns('',
                       url(r'^$', contact, name='contact'),
)
