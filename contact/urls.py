# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url
from contact.views import general
urlpatterns = patterns(
    '',
    url(r'^$', general, name='contact'),
)
