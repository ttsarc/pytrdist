# -*- encoding: utf-8 -*-

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.conf import settings
from accounts.views import company_index, company_detail, company_entry

urlpatterns = patterns('',
                       url(r'^$', company_index, name='company_index'),
                       url(r'^entry$', company_entry, name='company_entry'),
                       url(r'^(?P<company_id>\d+)$', company_detail, name='company_detail'),
)
