# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from accounts.views import (
    mypage_edit_profile,
    mypage_edit_company,
    mypage_home, )
from documents import views as documents
from seminars import views as seminars
from django.contrib.auth import views as auth_views
from registration.views import change_email, change_email_done
urlpatterns = patterns(
    '',
    url(r'^$', mypage_home, name='mypage_home'),
    url(r'^profile/edit$', mypage_edit_profile, name='mypage_edit_profile'),
    url(r'^company/edit$', mypage_edit_company, name='mypage_edit_company'),
    #documents
    url(r'^documents/add$', documents.add, name='document_add'),
    url(
        r'^documents/edit/(?P<document_id>\d+)$',
        documents.edit,
        name='document_edit'),
    url(
        r'^documents/edit$',
        documents.edit_index,
        name='document_edit_index'),
    url(
        r'^documents/leads$',
        documents.download_log,
        name='document_leads_index'),
    url(
        r'^documents/leads/(?P<page>\d+)$',
        documents.download_log,
        name='document_leads_paging'),
    url(
        r'^documents/leads/csv$',
        documents.download_log,
        {'type': 'csv'},
        name='document_leads_csv'),
    url(
        r'^history/document$',
        documents.my_download_history,
        name='mypage_download_history'),
    #seminars
    url(
        r'^seminars/add$',
        seminars.add,
        name='seminar_add'),
    url(
        r'^seminars/edit/(?P<seminar_id>\d+)$',
        seminars.edit,
        name='seminar_edit'),
    url(
        r'^seminars/edit$',
        seminars.edit_index,
        name='seminar_edit_index'),
    url(
        r'^seminars/leads$',
        seminars.entry_log,
        name='seminar_leads_index'),
    url(
        r'^seminars/leads/(?P<page>\d+)$',
        seminars.entry_log,
        name='seminar_leads_paging'),
    url(
        r'^seminars/leads/csv$',
        seminars.entry_log,
        {'type': 'csv'},
        name='seminar_leads_csv'),
    url(
        r'^history/seminar$',
        seminars.my_entry_history,
        name='mypage_entry_history'),
    #changing
    url(r'^password/change$',
        auth_views.password_change,
        name='auth_password_change'),
    url(r'^password/change/done$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^email/change/send$',
        TemplateView.as_view(
            template_name='registration/change_email_send.html'),
        name='registration_change_email_send'),
    url(r'^email/change/complete$',
        TemplateView.as_view(
            template_name='registration/change_email_complete.html'),
        name='registration_change_email_complete'),
    url(r'^email/change/(?P<activation_key>\w+)$',
        change_email_done,
        name='registration_change_email_done'),
    url(r'^email/change$',
        change_email,
        {'backend': 'registration.backends.default.DefaultBackend'},
        name='registration_change_email'),
)
