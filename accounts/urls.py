# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = patterns(
    '',
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^password/reset$',
        auth_views.password_reset,
        {'from_email': settings.SERVER_EMAIL},
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
)
