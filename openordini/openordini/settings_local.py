from openordini.openordini.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'openordini',
        'NAME': 'openordini',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}

ROOT_URLCONF = 'openordini.openordini.urls_local'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'django_cas.middleware.CASMiddleware',
)

CAS_SERVER_URL = 'http://localhost:8080/cas/'
