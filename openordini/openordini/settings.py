from open_municipio.settings import *

DOMAIN_ROOT = os.path.abspath(os.path.dirname(os.path.dirname((os.path.dirname(__file__)))))
# root directory for this Django project (on the server machine)
PROJECT_ROOT = os.path.join(DOMAIN_ROOT, 'openordini')
REPO_ROOT = os.path.abspath(os.path.dirname(PROJECT_ROOT))

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

TEMPLATE_LOADERS = (
    'apptemplates.Loader',
) + TEMPLATE_LOADERS

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
) + TEMPLATE_DIRS

INSTALLED_APPS = INSTALLED_APPS + (
    'payments',   
    'open_municipio',
    'openordini.oo_payments',
)

ROOT_URLCONF = 'openordini.urls'

MEDIA_ROOT = os.path.join(DOMAIN_ROOT, 'public', 'media')
STATIC_ROOT = os.path.join(DOMAIN_ROOT, 'public', 'static')

STATICFILES_DIRS += (
    os.path.join(PROJECT_ROOT, 'static'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'console-import':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'logfile': {
            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
            'class':'logging.FileHandler',
            'filename': os.path.join(DOMAIN_ROOT,"log","logfile"),
#            'maxBytes': 5 * 1024 * 1024,
#            'backupCount': 10,
            'formatter': 'standard',
            },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'webapp': {
            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
            'class':'logging.FileHandler',
            'filename': REPO_ROOT + "/log/webapp.log",
#            'maxBytes': 50000,
#            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        'import': {
            'handlers': ['console-import', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
            },
        'webapp': {
            'handlers': [ 'webapp', ],
            'level': 'DEBUG',
            'propagate': True,
            }, 
                
    }
}

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

PAYMENT_BASE_URL = 'http://localhost:8000/'

PAYMENT_MODEL = 'oo_payments.Payment'

PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {})}
