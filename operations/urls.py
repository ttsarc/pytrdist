# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url
from operations.views import company_leads, download_leads

urlpatterns = patterns(
    '',
    url(
        r'^$',
        company_leads,
        name='operation_company_leads'),
    url(
        r'^lead/(?P<company_id>\d+)/(?P<log_type>.+)/csv$',
        download_leads,
        {'type': 'csv'},
        name='operation_download_leads'),
    url(
        r'^lead/(?P<company_id>\d+)/(?P<log_type>.+)/$',
        download_leads,
        name='operation_show_leads'),
    url(
        r'^lead/(?P<company_id>\d+)/(?P<log_type>.+)/(?P<page>\d+)$',
        download_leads,
        name='operation_show_leads_paging'),
)
