from openordini.openordini.settings import *

ROOT_URLCONF = 'openordini.openordini.urls_staging'

ALLOWED_HOSTS = [ 'ordine.psicologipuglia.it', ]

DEBUG = False
TEMPLATE_DEBUG = False

MANAGERS = (
    ('Antonio Vangi', 'antonio.vangi.av@gmail.com'),
    ('Francesco Spegni', 'francesco.spegni@gmail.com'),
)

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

PAYMENT_BASE_URL = 'http://%s/' % ALLOWED_HOSTS[0]

PAYMENT_VARIANTS = {
    'default': ('payments.paypal.PaypalProvider', {
        'client_id': 'xxx',
        'secret': 'xxx',
        'endpoint': 'https://api.sandbox.paypal.com',
        'capture': False,
    })}

UI_ALLOW_NICKNAMES = False

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr',
        'URL': 'http://127.0.0.1:8080/solr/oo',
        'TIMEOUT': 300, # 5 minutes
        'BATCH_SIZE': 100,
        'SEARCH_RESULTS_PER_PAGE': 10,
    }
}

