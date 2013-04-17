# -*- encoding: utf-8 -*-

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from accounts.views import mypage_edit_profile, mypage_edit_company, mypage_home
from documents.views import add, edit, edit_index, download_log,my_download_history
from django.contrib.auth import views as auth_views
from registration.views import change_email,change_email_done
urlpatterns = patterns('',
                       url(r'^$', mypage_home, name='mypage_home'),
                       url(r'^profile/edit$', mypage_edit_profile, name='mypage_edit_profile'),
                       url(r'^company/edit$', mypage_edit_company, name='mypage_edit_company'),
                       url(r'^documents/add$', add, name='document_add'),
                       url(r'^documents/edit/(?P<document_id>\d+)$', edit, name='document_edit'),
                       url(r'^documents/edit$', edit_index, name='document_edit_index'),
                       url(r'^documents/leads$', download_log, name='document_leads_index'),
                       url(r'^documents/leads/(?P<page>\d+)$', download_log, name='document_leads_paging'),
                       url(r'^documents/leads/csv$', download_log, {'type':'csv'}, name='document_leads_csv'),
                       url(r'^history/document$', my_download_history, name='mypage_download_history'),
                       url(r'^password/change$',
                           auth_views.password_change,
                           name='auth_password_change'),
                       url(r'^password/change/done$',
                           auth_views.password_change_done,
                           name='auth_password_change_done'),
                       url(r'^email/change/send$',
                           TemplateView.as_view(template_name='registration/change_email_send.html'),
                           name='registration_change_email_send'),
                       url(r'^email/change/complete$',
                           TemplateView.as_view(template_name='registration/change_email_complete.html'),
                           name='registration_change_email_complete'),
                       url(r'^email/change/(?P<activation_key>\w+)$',
                           change_email_done,
                           name='registration_change_email_done'),
                       url(r'^email/change$',
                           change_email,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_change_email'),
)
