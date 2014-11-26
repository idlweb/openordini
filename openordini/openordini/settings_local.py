from openordini.openordini.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'openordini',
        'NAME': 'ooantonio',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}

ROOT_URLCONF = 'openordini.openordini.urls_local'

#CAS_SERVER_URL = 'http://localhost:8000/cas/'
