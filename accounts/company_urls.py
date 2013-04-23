# -*- encoding: utf-8 -*-

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.conf import settings
from accounts.views import company_index, company_detail

urlpatterns = patterns('',
                       url(r'^$', company_index, name='company_index'),
                       url(r'^(?P<company_id>\d+)$', company_detail, name='company_detail'),
)
