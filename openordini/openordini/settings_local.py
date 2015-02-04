from openordini.openordini.settings import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openordini',
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

LEAFLET_CONFIG = {
    #'SPATIAL_EXTENT': (5.0, 45.0, 7.5, 46)
    'DEFAULT_CENTER': (50.5, 30.5),
    'DEFAULT_ZOOM': 16,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 8,
}

UI_ALLOW_NICKNAMES = False
