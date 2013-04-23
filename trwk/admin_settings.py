from settings import *
INSTALLED_APPS += (
    'django.contrib.admin',
    'operations',
)
ADMIN = True
DEBUG = True

TEMPLATE_CONTEXT_PROCESSORS += (
    "trwk.context_processor.admin",
)

