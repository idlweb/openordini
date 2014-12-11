from openordini.openordini.settings import *

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

CAS_SERVER_URL = 'http://localhost:8080/cas/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
