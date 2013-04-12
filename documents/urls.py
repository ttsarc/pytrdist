# -*- encoding: utf-8 -*-
try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from documents.views import detail, preview, download, index, send, download_complete

urlpatterns = patterns('',
                       #url(r'^add/$', add, name='document_add'),
                       #url(r'^edit/(?P<document_id>\d+)/$', edit, name='document_edit'),
                       #url(r'^edit/$', edit_index, name='document_edit_index'),
                       url(r'^detail/(?P<document_id>\d+)/$', detail, name='document_detail'),
                       url(r'^preview/(?P<document_id>\d+)/$', preview, name='document_preview'),
                       url(r'^download/link/(?P<id_sign>[a-zA-Z0-9_\-:]+)/$', send, name='document_download_link'),
                       url(r'^download/(?P<document_id>\d+)/$', download, name='document_download'),
                       url(r'^download/complete/(?P<id_sign>[a-zA-Z0-9_\-:]+)/$', download_complete, name='document_download_complete'),
                       url(r'^$', index, name='document_index'),
)
