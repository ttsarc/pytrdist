# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url
from documents.views import (
    detail,
    preview,
    download,
    index,
    download_link,
    download_complete)
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
reverse_lazy = lazy(reverse, str)

urlpatterns = patterns(
    '',
    url(
        r'^detail/(?P<document_id>\d+)$',
        detail,
        name='document_detail'),
    url(
        r'^preview/(?P<document_id>\d+)$',
        preview,
        name='document_preview'),
    url(
        r'^category/(?P<category_id>\d+)$',
        index,
        name='document_category_index'),
    url(
        r'^category/(?P<category_id>\d+)/page/(?P<page>\d+)$',
        index,
        name='document_category_paged'),
    url(
        r'^ranking$',
        index,
        name='document_ranking_index'),
    url(
        r'^ranking/page/(?P<page>\d+)$',
        index,
        name='document_ranking_paged'),
    url(
        r'^page/1$',
        RedirectView.as_view(url=reverse_lazy('document_index'))),
    url(
        r'^page/(?P<page>\d+)$',
        index,
        name='document_paged'),
    url(
        r'^$',
        index,
        name='document_index'),
    url(
        r'^download/(?P<document_id>\d+)$',
        download,
        name='document_download'),
    url(
        r'^download/link/(?P<id_sign>[a-zA-Z0-9_\-:]+)$',
        download_link,
        name='document_download_link'),
    url(
        r'^download/complete/(?P<id_sign>[a-zA-Z0-9_\-:]+)$',
        download_complete,
        name='document_download_complete'),
)
