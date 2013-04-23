from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings

# Uncomment the next two lines to enable the admin:


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trwk.views.home', name='home'),
    # url(r'^trwk/', include('trwk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$',          TemplateView.as_view(template_name='base.html'), name='home'),
    #url(r'^admin/',     include(admin.site.urls)),
    url(r'^accounts/',  include('registration.backends.default.urls')),
    url(r'^accounts/',  include('accounts.urls')),
    url(r'^company/',   include('accounts.company_urls')),
    url(r'^mypage/',    include('mypage.urls')),
    url(r'^documents/', include('documents.urls')),
    url(r'^seminars/',  include('seminars.urls')),
    url(r'^contact/',   include('contact.urls')),
    #url(r'^operations/',include('operations.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    )
if settings.ADMIN:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        url(r'^admin/',     include(admin.site.urls)),
        url(r'^operations/',include('operations.urls')),
    )
