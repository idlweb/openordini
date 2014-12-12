from openordini.openordini.settings import *

ROOT_URLCONF = 'openordini.openordini.urls_staging'

ALLOWED_HOSTS = [ 'oo.psicologipuglia.it', ]

INSTALLED_APPS = INSTALLED_APPS + (
    'mama_cas',
    'django_cas_ng',
)

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
    'django_cas_ng.backends.CASBackend',

)

CAS_IGNORE_REFERER = False
CAS_LOGOUT_COMPLETELY = True
#CAS_GATEWAY_PARAMETER = "gateway"
#CAS_GATEWAY_LOOP_PARAMETER = "gateway"
#CAS_USER_DETAILS_RESOLVER = CAS_populate_user

CAS_SERVER_URL = 'http://%s/cas/' % ALLOWED_HOSTS[0]
