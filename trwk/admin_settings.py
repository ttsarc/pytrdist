from settings import *
INSTALLED_APPS += (
    'django.contrib.admin',
    'operations',
)
ADMIN = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SSL_URLS = (
    '^/dummy/',
)
SSL_IGNORE_URLS = (
    '^/dummy2/',
)

