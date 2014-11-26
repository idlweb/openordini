from openordini.openordini.settings import *

ROOT_URLCONF = 'openordini.openordini.urls_staging'

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

MEDIA_ROOT = os.path.join(REPO_ROOT, '..', 'public', 'media')
STATIC_ROOT = os.path.join(REPO_ROOT, '..', 'public', 'static')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'django_cas.middleware.CASMiddleware',
)

CAS_SERVER_URL = 'http://www.psicologipuglia.it/cas/'
