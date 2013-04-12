# -*- encoding: utf-8 -*-

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.views.generic import TemplateView
#from accounts.views import mypage_edit_profile, mypage_edit_company, mypage_home
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       #url(r'^mypage/complete/$',
                       #    TemplateView.as_view(template_name='registration/activation_complete.html'),
                       #    name='registration_activation_complete'),
                       #url(r'^mypage/edit/profile/$', mypage_edit_profile, name='mypage_edit_profile'),
                       #url(r'^mypage/edit/company/$', mypage_edit_company, name='mypage_edit_company'),
                       #url(r'^mypage/$', mypage_home, name='mypage_home'),
                       url(r'^login/$',
                           auth_views.login,
                           {'template_name': 'registration/login.html'},
                           name='auth_login'),
                       url(r'^logout/$',
                           auth_views.logout,
                           {'template_name': 'registration/logout.html'},
                           name='auth_logout'),
                       #url(r'^password/change/$',
                       #    auth_views.password_change,
                       #    name='auth_password_change'),
                       #url(r'^password/change/done/$',
                       #    auth_views.password_change_done,
                       #    name='auth_password_change_done'),
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           name='auth_password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='auth_password_reset_confirm'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='auth_password_reset_complete'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='auth_password_reset_done'),
)
