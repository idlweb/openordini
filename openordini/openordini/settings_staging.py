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

