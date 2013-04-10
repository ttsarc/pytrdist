# -*- encoding: utf-8 -*-
try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from documents.views import add, edit, edit_index, detail, download, index, send

urlpatterns = patterns('',
                       url(r'^add/$', add, name='document_add'),
                       url(r'^edit/(?P<document_id>\d+)/$', edit, name='document_edit'),
                       url(r'^edit/$', edit_index, name='document_edit_index'),
                       url(r'^detail/(?P<document_id>\d+)/$', detail, name='document_detail'),
                       url(r'^download/(?P<document_id>\d+)/$', download, name='document_download'),
                       url(r'^download/link/(?P<download_sign>[a-zA-Z0-9_\-:]+)/$', send, name='document_download_link'),
                       url(r'^$', index, name='document_index'),
)
