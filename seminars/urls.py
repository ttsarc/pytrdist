# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url
from seminars.views import detail, preview, entry, index, entry_complete
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
reverse_lazy = lazy(reverse, str)

urlpatterns = patterns(
    '',
    url(
        r'^detail/(?P<seminar_id>\d+)$',
        detail,
        name='seminar_detail'),
    url(
        r'^preview/(?P<seminar_id>\d+)$',
        preview,
        name='seminar_preview'),
    url(
        r'^category/(?P<category_id>\d+)$',
        index,
        name='seminar_category_index'),
    url(
        r'^category/(?P<category_id>\d+)/page/(?P<page>\d+)$',
        index,
        name='seminar_category_paged'),
    url(
        r'^ranking$',
        index,
        name='seminar_ranking_index'),
    url(
        r'^ranking/page/(?P<page>\d+)$',
        index,
        name='seminar_ranking_paged'),
    url(
        r'^page/1$',
        RedirectView.as_view(url=reverse_lazy('seminar_index'))),
    url(
        r'^page/(?P<page>\d+)$',
        index,
        name='seminar_paged'),
    url(
        r'^$',
        index,
        name='seminar_index'),
    url(
        r'^entry/(?P<seminar_id>\d+)$',
        entry,
        name='seminar_entry'),
    url(
        r'^entry/complete/(?P<seminar_id>[a-zA-Z0-9_\-:]+)$',
        entry_complete,
        name='seminar_entry_complete'),
)
