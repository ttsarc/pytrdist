"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

"""

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from registration.views import activate
from registration.views import register
from registration.views import change_email,change_email_done

urlpatterns = patterns('',
                       url(r'^activate/complete/$',
                           TemplateView.as_view(template_name='registration/activation_complete.html'),
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_activate'),
                       url(r'^register/$',
                           register,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_register'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='registration/registration_complete.html'),
                           name='registration_complete'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='registration_disallowed'),
                       #change_email
                       url(r'^change_email/send/$',
                           TemplateView.as_view(template_name='registration/change_email_send.html'),
                           name='registration_change_email_send'),
                       url(r'^change_email/complete/$',
                           TemplateView.as_view(template_name='registration/change_email_complete.html'),
                           name='registration_change_email_complete'),
                       url(r'^change_email/(?P<activation_key>\w+)/$$',
                           change_email_done,
                           name='registration_change_email_done'),
                       url(r'^change_email/$',
                           change_email,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_change_email'),
                       #auth
                       #(r'', include('registration.auth_urls')),
                       )
