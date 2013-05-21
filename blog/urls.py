# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url
from blog.views import detail, index
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
reverse_lazy = lazy(reverse, str)

urlpatterns = patterns(
    '',
    url(
        r'^detail/(?P<slug>[a-z0-9\-]+)$',
        detail,
        name='post_detail'),
    url(
        r'^category/(?P<category_id>\d+)$',
        index,
        name='post_category_index'),
    url(
        r'^category/(?P<category_id>\d+)/page/(?P<page>\d+)$',
        index,
        name='post_category_paged'),
    url(
        r'^page/1$',
        RedirectView.as_view(url=reverse_lazy('post_index'))),
    url(
        r'^page/(?P<page>\d+)$',
        index,
        name='post_paged'),
    url(
        r'^$',
        index,
        name='post_index'),
)
