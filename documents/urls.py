# -*- encoding: utf-8 -*-
try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from documents.views import add, edit, edit_index

urlpatterns = patterns('',
                       url(r'^add/$', add, name='document_add'),
                       url(r'^edit/(?P<document_id>\d+)/$', edit, name='document_edit'),
                       url(r'^edit/$', edit_index, name='document_edit_index'),
)
