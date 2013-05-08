# -*- encoding: utf-8 -*-
# Django settings for trwk project.

DEBUG = False
ADMIN = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('example', 'trwk@example.com'),
)

SERVER_EMAIL = 'noreply@example.com'
CONTACT_EMAIL = 'contact@example.com'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'trwk',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'trwk_user',
        'PASSWORD': 'password',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

import os
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ja-JP'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT =  os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT =  os.path.join(SITE_ROOT, 'static_root')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'h&zl5f-lx1%n%gju*8d%w+to*!jev_pqg6$zd5o1=6*iam2&@9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'beproud.django.ssl.middleware.SSLProxyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'beproud.django.ssl.middleware.SSLRedirectMiddleware',
)

ROOT_URLCONF = 'trwk.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'trwk.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    #'gunicorn',
    'sorl.thumbnail',
    'accounts',
    'documents',
    'seminars',
    'registration',
    'mypage',
    'contact',
    'sites',
    'search',
    'icybackup',
    'bootstrap-pagination',
    'blog',
    'beproud.django.ssl',
)
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "trwk.context_processor.admin",
)
ITEMS_PER_PAGE = 5
POSTS_PER_PAGE = 5
DOCUMENTS_PER_PAGE = 5
SEMINARS_PER_PAGE = 5
LOGS_PER_PAGE = 10

#Postの記事内に埋め込むサムネイルサイズ
POST_THUMBNAIL_SIZE ='240x240'

AUTH_USER_MODEL = 'accounts.MyUser'
AUTH_PROFILE_MODULE = 'accounts.MyUserProfile'

ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_HOST = 'localhost'

LOGIN_REDIRECT_URL = '/'

BAD_EMAIL_DOMAIN = [
    'biz.ezweb.ne.jp',
    'c.vodafone.ne.jp',
    'd.vodafone.ne.jp',
    'di.pdx.ne.jp',
    'disney.ne.jp',
    'disney.ne.jp',
    'dj.pdx.ne.jp',
    'dk.pdx.ne.jp',
    'dwmail.jp',
    'ezweb.ne.jp',
    'h.vodafone.ne.jp',
    'ido.ne.jp',
    'jp-c.ne.jp',
    'jp-d.ne.jp',
    'jp-h.ne.jp',
    'jp-k.ne.jp',
    'jp-n.ne.jp',
    'jp-q.ne.jp',
    'jp-r.ne.jp',
    'jp-s.ne.jp',
    'jp-t.ne.jp',
    'k.vodafone.ne.jp',
    'n.vodafone.ne.jp',
    'pdx.ne.jp',
    'q.vodafone.ne.jp',
    'r.vodafone.ne.jp',
    's.vodafone.ne.jp',
    'sky.tkc.ne.jp',
    'sky.tkk.ne.jp',
    'sky.tu-ka.ne.jp',
    'softbank.ne.jp',
    't.vodafone.ne.jp',
    'vertuclub.ne.jp',
    'vodafone.ne.jp',
    'willcom.com',
    'wm.pdx.ne.jp',
    'docomo.ne.jp',
    'yahoo.co.jp',
    #'gmail.com',
    'hotmail.com',
]

THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'
THUMBNAIL_DEBUG = False
DEFAULT_THUMBNAIL = os.path.join(SITE_ROOT, 'static', 'images', 'thumb-400x300.png')


SSL_URLS = (
    '^/mypage/',
    '^/operation/',
    '^/documents/download/',
    '^/seminars/entry/',
    '^/accounts/',
    '^/contact/',
)
SSL_IGNORE_URLS = (
    '^/static/',
    '^/media/',
)

try:
    from trwk.local_settings import *
except:
    pass
