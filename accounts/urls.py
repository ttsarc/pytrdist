# -*- encoding: utf-8 -*-

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from accounts.views import mypage_edit_profile, mypage_edit_company, mypage_home

urlpatterns = patterns('',
                       #url(r'^mypage/complete/$',
                       #    TemplateView.as_view(template_name='registration/activation_complete.html'),
                       #    name='registration_activation_complete'),
                       url(r'^mypage/edit/profile/$', mypage_edit_profile, name='mypage_edit_profile'),
                       url(r'^mypage/edit/company/$', mypage_edit_company, name='mypage_edit_company'),
                       url(r'^mypage/$', mypage_home, name='mypage_home'),
)
