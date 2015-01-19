from openordini.openordini.settings import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openordini_antonio',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}

ROOT_URLCONF = 'openordini.openordini.urls_local'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PAYMENT_BASE_URL = 'http://localhost:8000/'

PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {})}

